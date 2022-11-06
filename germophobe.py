# import pygame module in this program
import pygame
import random
import time
import threading



def render_multiline(data):
        "Shows a multiline string with text, y pos and color for each line separated by comma"
        tc = []
        for line in data.split("\n"):
 
            if line != "":
                text, height, color = line.split(",")
                if height == " " or height == "":
                    height = 0
                    if color == " " or color == "":
                        color = "red"
                else:
                    height = int(height)
                tc.append([text, height, color])
        # 2. Each list of the list above is send to write to render text
        cnt = 0
        for t, height, c in tc:
            cnt += 30
            # calls write passing the text, the vertical position and the color
            for i in t.split("\n"):
                if height == 0:
                    height = cnt
                write(i, 200, height, color=c)
                height += 30
 
"""
INSERT:
text, vertical position, color
 
1. you can omit the vertical position
2. To put a blank line use ,,
"""
TEXT1 = """*** GERMAPHOBE ***, , gold
A Game by Holden and Matt, , red
,,
https://github.com/holdena12/germophobe, , coral
Game vaguely inspired by fear of germs, , cyan
,,
PRESS ANY KEY TO PLAY, , green
Press left arrow to go left, , blue
Press right arrow to go right ,, blue
Press space to shoot vaccines ,, blue
Press c for instant doom,, red

"""

pygame.init()

Font = pygame.font.SysFont
font1 = Font("Arial", 24)
font2 = Font("Arial", 20)

def write(text, x, y, color="Coral",):
    "Returns a surface with a text in the center of the screen, at y coord."
    
    surface_text = font1.render(text, 1, pygame.Color(color))
    text_rect = surface_text.get_rect(center=(500 // 2, y))
    win.blit(surface_text, text_rect)
    return surface_text


#the players score
score = 0

rounds = 10

lives = 1
keys = pygame.key.get_pressed()
powerUpSpread = random.randint(7,15)
germRNot = 4
vaccineSpread = 0
BOARD_WIDTH = 800
BOARD_HEIGHT = 1100
gameTop = pygame.Rect(0,0,BOARD_WIDTH,1)
gameBottom = pygame.Rect(0,BOARD_HEIGHT,BOARD_WIDTH,1)
gameLeft = pygame.Rect(0,0,1,BOARD_HEIGHT)
gameRight= pygame.Rect(BOARD_WIDTH,0,1,BOARD_HEIGHT)
currentColor = (0, 0, 255)
obstColor = (0,0, 0)
obst2Color = (255,255,255)

level = 1


win = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))

class GameObject:

    dead = False
    collisionBuffer = 0

    def __init__(self, color, rect: pygame.Rect, vel , xdir =1, ydir =1, isBaby = True, xPert = 1, yPert = 1) -> None:
        self.rect = rect
        self.vel = vel
        self.xdir = xdir
        self.ydir = ydir
        self.color = color
        self.isBaby = isBaby
        self.dead = False
        self.xPert = xPert
        self.yPert = yPert
   

    def setDead(self):
        self.dead = True

class PowerUps(GameObject):
  def __init__(self, color, rect: pygame.Rect, vel, xdir =1, ydir =1, isBaby = True, xPert = 1, yPert = 1, type = 0):
    GameObject.__init__(self,color, rect , vel , xdir, ydir , isBaby , xPert , yPert)
    self.type = type
    #add properties etc.


# activate the pygame library .  
# initiate pygame and give permission  
# to use pygame's functionality.  



font = pygame.font.Font('freesansbold.ttf', 16)
# create the display surface object  
# of specific dimension..e(500, 500).  

 
# set the pygame window name
pygame.display.set_caption("GermoPhobe...")

playerSpeed = 13


player_width = 100
player = GameObject((50,50,75), pygame.Rect((BOARD_WIDTH/2), BOARD_HEIGHT-80, player_width, 80),playerSpeed,0,0)  
activeGerms = []
activePowerUps = []
obstacles = []
vaccines = []
activeWeirdGerms = []
# create obstacles
obstacle = GameObject(obstColor, pygame.Rect(200,500,200,25), 10)
obstacle2 = GameObject(obst2Color,pygame.Rect(200,300,150,25), 8, -1, 0)
obstacles.append(obstacle)
obstacles.append(obstacle2)



class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True



  def stop(self):
    self._timer.cancel()
    self.is_running = False

white = (255,255,255)
blue = (0,0,255)

#vaccine = GameObject((255,165,0), pygame(player.rect.width-player.rect.width/2,player.rect.center, 0,0),0,0)


   
def shootVaccine(vaccine):
   
    vaccine.vel = 10
    vaccine.ydir = -1

    vaccines.append(vaccine)
       
isWeirdGerm = random.randint(1,6)
germSpeed = random.uniform(4,5)
def addWeirdGerms():
    weirdGerm = GameObject((255,0,150), pygame.Rect(random.randint(25,BOARD_WIDTH-25), germSpeed, 50, 10,25),3)
    activeWeirdGerms.append(weirdGerm)
   
def addGerm():
    isWeirdGerm = random.randint(1,6)
    germ = GameObject((50,255,0), pygame.Rect(random.randint(25,BOARD_WIDTH-25), 50, 25,25),random.randint(3,6),3)
    activeGerms.append(germ)
    if isWeirdGerm == 1:
            isWeirdGerm = True
            germ.color = (255,0,0)
            germ.vel = (random.uniform(6,10))


def addPowerUp():
    powerUpType = random.randint(0,2)
    

    powerUp = PowerUps((0,255,255), pygame.Rect(random.randint(25,775), 50, 25,25),random.randint(5,7),random.choices([-1,1]),1,True,1,1,powerUpType)
    if powerUpType == 1:
        powerUp.color = (255,255,255)
    if powerUpType == 2:
        powerUp.color = (0,0,0)

    activePowerUps.append(powerUp)


def updateMovingObject(gameObject: GameObject, obstacles =[],dieOnImpact = False):
    if gameObject.isBaby == True:
        gameObject.isBaby = False
        rand = random.randint(0,1)
        if rand == 0:
            gameObject.xdir = -1
        else:
            gameObject.xdir = 1
   
    if gameObject.collisionBuffer>0:
        gameObject.collisionBuffer -= 1

   # detect if object hits a side wall
    if (gameObject.rect.colliderect(gameRight)):
        gameObject.xdir = gameObject.xdir * -1
    elif (gameObject.rect.colliderect(gameLeft)):
        gameObject.xdir = gameObject.xdir * -1
    elif gameObject.ydir == -1 and gameObject.rect.y <= gameObject.rect.height:
        gameObject.collisionBuffer = 0
        gameObject.ydir *= -1
        if (dieOnImpact):
            gameObject.dead = True
            return True
    # detect if object hits an obstacle
    if gameObject.collisionBuffer == 0:
        for obstacle in obstacles:
            if gameObject.rect.colliderect(obstacle):
                if (dieOnImpact):
                    gameObject.dead = True
                    return True
                gameObject.collisionBuffer = 60
                gameObject.ydir *= -1
               
                if isWeirdGerm == True:
                    if gameObject.rect.colliderect(obstacle):
                     
                        gameObject.ydir *= -1
           
                #if (gameObject.rect.left <= obstacle.left+gameObject.rect.width/2):
                    #gameObject.xdir *= -1
                #pick a random number between 1 and 1.5 and random boolean 0 or 1 to indicate positve or negative and then set that value to gameObject.xPert
                # pick a random number between 1 and 1.5 and random boolean 0 or 1 to indicate positve or negative and then set that value to gameObject.yPert
              
                gameObject.xPert = random.uniform(1,1.5)
                gameObject.yPert = random.uniform(1,1.5)
               
                #print("Obstacle contact new pertubation is xPert {} and yPert {}".format(gameObject.xPert, gameObject.yPert))
   
    gameObject.rect = gameObject.rect.move(gameObject.xdir*gameObject.vel*gameObject.xPert, gameObject.ydir*gameObject.vel*gameObject.yPert)
       
 
    pygame.draw.rect(win, gameObject.color, gameObject.rect)
    return gameObject.dead


timers = []
rt = RepeatedTimer(germRNot, addGerm)
rpt = RepeatedTimer(powerUpSpread, addPowerUp)
timers.append(rt)
timers.append(rpt)
addGerm()


def detectGermKill(germ, gameObject):
    global score
    global level
    global germSpeed
    global germRNot
    global rt
    if (gameObject.rect.colliderect(germ.rect)):
        score += 1
        if (score % 5 == 0 ):
            level += 1
            germSpeed += 1

            gameObject.rect.width = player_width
            germRNot -= .2 * germRNot
            if germRNot <= 1:
                germRNot = 1
            rt.stop()
            timers.remove(rt)
            rt = RepeatedTimer(germRNot, addGerm)
            timers.append(rt)
        gameObject.rect.width = gameObject.rect.width-15
        if gameObject.rect.width <= 20:
            gameObject.rect.width =20
        germ.dead = True    
    return germ.dead 

 
# Indicates pygame is running
run = True
lastFireTime = -1

clock = pygame.time.Clock()
def mainloop():
    global clock, font1, font2
    # infinite loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
            elif event.type == pygame.KEYDOWN:
                playGame()
        render_multiline(TEXT1)
        clock.tick(30)
        pygame.display.update()

def quitGame():
    for timer in timers:
        timer.stop()
    pygame.quit()
    exit()

def playGame():
    global run, liveString, roundsString, levelString, lives, rounds, lastFireTime, keys, rt
    while run:
        # creates time delay of 10ms
        pygame.time.delay(10)
        
        # iterate over the list of Event objects  
        # that was returned by pygame.event.get() method.
        for event in pygame.event.get():
        
            # if event object type is QUIT  
            # then quitting the pygame  
            keys = pygame.key.get_pressed()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    lastFireTime = -1
            if event.type == pygame.QUIT:
                quitGame()

       
        if (keys[pygame.K_SPACE] and rounds > 0):

            currentTime = round(time.time()*1000)
            if (lastFireTime < 0  or currentTime-lastFireTime > 1500):
                rounds -=1
                lastFireTime = currentTime
                vaccine = GameObject((255, 153, 51), pygame.Rect((player.rect.x + player.rect.width/2), player.rect.y, 10, 45),0,0,0)
                shootVaccine(vaccine)
        
        # if left arrow key is pressed
        if keys[pygame.K_LEFT] and player.rect.x>0:
            
            # decrement in x co-ordinate
            player.rect = player.rect.move(-1*player.vel,0)
        
            
        # if left arrow key is pressed
        if keys[pygame.K_RIGHT] and player.rect.x<BOARD_WIDTH-player.rect.width:
            
            # increment in x co-ordinate
            player.rect = player.rect.move(player.vel,0)


        #shootVaccine()

        # covid easter egg
        if keys[pygame.K_c]:
            lives=7
            playerSpeed = 25
            # let the chaos begin!
            rt.stop()
            timers.remove(rt)
            rt = RepeatedTimer(.1, addGerm)
            timers.append(rt)





        win.fill(currentColor)
        for obstacle in obstacles:
            obstacle.ydir = 0
            updateMovingObject(obstacle)
            pygame.draw.rect(win, obstColor, obstacle)
        
        for vaccine in vaccines:
            if (vaccine.dead == False):
                # only update object if it is not dead
                if (updateMovingObject(vaccine, obstacles, True) == False):
                    vaccine.xdir = 0
                    vaccine.vel = 15
                    pygame.draw.rect(win,vaccine.color,vaccine.rect)
            else:
                vaccines.remove(vaccine)

        # velocity / speed of movement
        scoreString = "Score: {}".format(score)
        text = font.render(scoreString, True, white, blue)
        levelString = "level: {}".format(level)
        text2 = font.render(levelString, True, white, blue )
        liveString = "lives: {}".format(lives)
        text3 = font.render(liveString, True, white, blue )
        roundsString = "Rounds: {}".format(rounds)
        text4 = font.render(roundsString,True,white, blue)
        

    
        textRect = text.get_rect()
        text2Rect = text2.get_rect()
        text3Rect = text3.get_rect()
        text4Rect = text4.get_rect()
    
    
        # set the center of the rectangular object.
        textRect.center = (35,25)
        text2Rect.center = (765, 25)
        text3Rect.center = (35, 50)
        text4Rect.center = (755, 50)
        win.blit(text, textRect)
        win.blit(text2, text2Rect)
        win.blit(text3, text3Rect)
        win.blit(text4, text4Rect )

        # process active germs
    
        for germ in activeGerms:
        
            if (updateMovingObject(germ, obstacles) == True):
                activeGerms.remove(germ)
            # germ collision detection
            #if (germ.dead == False and germ.rect.colliderect(obstacle2.rect) or powerUp.dead == False and powerUp.rect.colliderect(obstacle2.rect) ):     
            if (germ.dead == False):
                if (detectGermKill(germ, player) == False):
                    for vaccine in vaccines:
                        if (detectGermKill(germ, vaccine) == True):
                            vaccine.dead = True
                            break

            if germ.dead == False and germ.rect.y >= BOARD_HEIGHT-germ.rect.height:
                germ.dead = True
                lives -=1

                if lives == 0:
                    print("Game Over...")
                    print("your score was",score ,". Level: ", level, " Good job!" )
                    run = False
                    quitGame()
                    break
        #process activePowerUps
        for powerUp in activePowerUps:
            if updateMovingObject(powerUp, obstacles) == True:
                activePowerUps.remove(powerUp)
            if powerUp.dead == False and player.rect.colliderect(powerUp.rect):
                powerUp.dead = True
                if powerUp.type == 0:
                    player.color =(255,255,0)
                    rounds +=5
                elif powerUp.type == 1:
                    lives +=1
                elif powerUp.type == 2:
                    player.rect.width = player.rect.width*3
                
            if powerUp.rect.y >= BOARD_HEIGHT-powerUp.rect.height:
                powerUp.dead = True
        
    
        # drawing object on screen which is rectangle here
        pygame.draw.rect(win, player.color, player.rect)
    

        # it refreshes the window
        pygame.display.update()

mainloop()
# closes the pygame window
quitGame()

exit()



