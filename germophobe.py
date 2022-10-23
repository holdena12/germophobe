# import pygame module in this program
import pygame
import random
import time
import threading
pygame.init()


#the players score
score = 0

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
obstacle2s = []
vaccines = []
activeWeirdGerms = []
# create obstacles
obstacle = GameObject(obstColor, pygame.Rect(200,500,400,50), 4)
obstacle2 = GameObject(obst2Color,pygame.Rect(200,300,200,50), 6)
obstacles.append(obstacle)
obstacle2s.append(obstacle2)



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
vaccine = GameObject((50,50,75), pygame.Rect((BOARD_WIDTH/2), BOARD_HEIGHT-105, 10, 15),0,0,0)

   
def shootVaccine():
   
 
    pygame.draw.rect(win,vaccine.color,vaccine.rect)
    vaccines.append(vaccine)
           
    vaccine.vel = 10


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
    powerUp = GameObject((10,75,200), pygame.Rect(random.randint(25,775), 50, 25,25),random.randint(5,7),3)
    activePowerUps.append(powerUp)

def updateFallingObject(gameObject: GameObject, obstacles =[]):
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
    # detect if object hits an obstacle
    if gameObject.collisionBuffer == 0:
        for obstacle in obstacles:
            if gameObject.rect.colliderect(obstacle):
                gameObject.collisionBuffer = 60
                rand_dir = random.randint(-1,5)
                if rand_dir == 0 or rand_dir == 2 or rand_dir == 3 or rand_dir == 4 or rand_dir == 5:
                    rand_dir =-1
                gameObject.ydir *= rand_dir
               
                if isWeirdGerm == True:
                    if gameObject.rect.colliderect(obstacle):
                        randDir = random.randint(-1,5)
                        if randDir == 0 or randDir == 1 or randDir == 2 or randDir == 3 or randDir == 4 or randDir == 5:
                            randDir = 1
                        gameObject.ydir *= randDir
            if gameObject.rect.colliderect(obstacle2):
                gameObject.collisionBuffer = 60
                rand_dir = random.randint(-1,5)
                if rand_dir == 0 or rand_dir == 2 or rand_dir == 3 or rand_dir == 4 or rand_dir == 5:
                    rand_dir =-1
                gameObject.ydir *= rand_dir
               
                if isWeirdGerm == True:
                    if gameObject.rect.colliderect(obstacle2):
                        randDir = random.randint(-1,5)
                        if randDir == 0 or randDir == 1 or randDir == 2 or randDir == 3 or randDir == 4 or randDir == 5:
                            randDir = 1
                        gameObject.ydir *= randDir

                #if (gameObject.rect.left <= obstacle.left+gameObject.rect.width/2):
                    #gameObject.xdir *= -1
                #pick a random number between 1 and 1.5 and random boolean 0 or 1 to indicate positve or negative and then set that value to gameObject.xPert
                # pick a random number between 1 and 1.5 and random boolean 0 or 1 to indicate positve or negative and then set that value to gameObject.yPert
                rand_sp = random.randint(0,1)
                if (rand_sp == 0):
                    rand_sp=-1
                else:
                    rand_sp = 1
                gameObject.xPert = random.uniform(1,1.5)*rand_sp
                gameObject.yPert = random.uniform(1,1.5)*rand_sp
               
                #print("Obstacle contact new pertubation is xPert {} and yPert {}".format(gameObject.xPert, gameObject.yPert))
   
    gameObject.rect = gameObject.rect.move(gameObject.xdir*gameObject.vel*gameObject.xPert, gameObject.ydir*gameObject.vel*gameObject.yPert)
       
 
    pygame.draw.rect(win, gameObject.color, gameObject.rect)
    return gameObject.dead


timers = []
rt = RepeatedTimer(germRNot, addGerm)
rpt = RepeatedTimer(powerUpSpread, addPowerUp)
addGerm()

 
# Indicates pygame is running
run = True
 
# infinite loop
while run:
    # creates time delay of 10ms
    pygame.time.delay(20)
     
    # iterate over the list of Event objects  
    # that was returned by pygame.event.get() method.  
    for event in pygame.event.get():
       
        # if event object type is QUIT  
        # then quitting the pygame  
      keys = pygame.key.get_pressed()
     
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
        lives=23
        playerSpeed = 25
        # let the chaos begin!
        rt.stop()
        rt = RepeatedTimer(.1, addGerm)





    win.fill(currentColor)
    for obstacle in obstacles:
        obstacle.ydir = 0
        updateFallingObject(obstacle)
        pygame.draw.rect(win, obstColor, obstacle)
    for obstacle2 in obstacle2s:
        obstacle2.ydir = 0
        updateFallingObject(obstacle2)
        pygame.draw.rect(win, obst2Color, obstacle2)

    # velocity / speed of movement
    scoreString = "Score: {}".format(score)
    text = font.render(scoreString, True, white, blue)
    levelString = "level: {}".format(level)
    text2 = font.render(levelString, True, white, blue )
    liveString = "lives: {}".format(lives)
   
    text3 = font.render(liveString, True, white, blue )
   
    textRect = text.get_rect()
    text2Rect = text2.get_rect()
    text3Rect = text3.get_rect()
   
   
    # set the center of the rectangular object.
    textRect.center = (35,25)
    text2Rect.center = (765, 25)
    text3Rect.center = (35, 50)
    win.blit(text, textRect)
    win.blit(text2, text2Rect)
    win.blit(text3, text3Rect)

    # process active germs
   
    for germ in activeGerms:
       
        if (updateFallingObject(germ, obstacles) == True):
            activeGerms.remove(germ)
        # germ collision detection
        #if (germ.dead == False and germ.rect.colliderect(obstacle2.rect) or powerUp.dead == False and powerUp.rect.colliderect(obstacle2.rect) ):

        if (germ.dead == False and player.rect.colliderect(germ.rect)):
            score += 1
            if (score % 5 == 0 ):
                level += 1
                germSpeed += 1
           
                player.rect.width = player_width
                germRNot -= .2 * germRNot
                if germRNot <= 1:
                    germRNot = 1
                rt.stop()
                rt = RepeatedTimer(germRNot, addGerm)
            player.rect.width = player.rect.width-15
            if player.rect.width <= 20:
                player.rect.width =20
            germ.dead = True      

         
        if germ.dead == False and germ.rect.y >= BOARD_HEIGHT-germ.rect.height:
            germ.dead = True
            lives -=1

            if lives == 0:
                print("Game Over...")
                print("your score was",score ,". Level: ", level, " Good job!" )
                run = False
                break
    #process activePowerUps
    for powerUp in activePowerUps:
        if updateFallingObject(powerUp, obstacles) == True:
            activePowerUps.remove(powerUp)
        if powerUp.dead == False and player.rect.colliderect(powerUp.rect):
            powerUp.dead = True
            lives +=1
        if powerUp.rect.y >= BOARD_HEIGHT-powerUp.rect.height:
            powerUp.dead = True
       
 
    # drawing object on screen which is rectangle here
    pygame.draw.rect(win, player.color, player.rect)
   

    # it refreshes the window
    pygame.display.update()

# closes the pygame window
pygame.quit()
rt.stop()
rpt.stop()

exit()



