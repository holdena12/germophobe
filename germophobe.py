# import pygame module in this program 
import pygame
import random
import time
import threading

#the players score
score = 0

lives = 1

powerUpSpread = random.randint(7,15)
germRNot = 4
BOARD_WIDTH = 800
BOARD_HEIGHT = 1100

class GameObject:

    dead = False

    def __init__(self, color, rect: pygame.Rect, vel, dir) -> None:
        self.rect = rect
        self.vel = vel
        self.dir = dir
        self.color = color
        self.dead = False

    def setDead(self):
        self.dead = True


# activate the pygame library .  
# initiate pygame and give permission  
# to use pygame's functionality.  
pygame.init()


font = pygame.font.Font('freesansbold.ttf', 16)
# create the display surface object  
# of specific dimension..e(500, 500).  
win = pygame.display.set_mode((BOARD_WIDTH,BOARD_HEIGHT))
  
# set the pygame window name 
pygame.display.set_caption("GermoPhobe...")

def drawPowerUp():
    pygame.draw.rect()


PLAYER_ORIG_WIDTH = 100
player = GameObject((50,50,50), pygame.Rect((BOARD_WIDTH/2), BOARD_HEIGHT-60, PLAYER_ORIG_WIDTH, 60),7,0)  
activeGerms = []
activePowerUps = []

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

def addGerm():
    germ = GameObject((50,255,0), pygame.Rect(random.randint(25,775), 50, 25,25),random.randint(3,5),3)
    activeGerms.append(germ)

def addPowerUp():
    powerUp = GameObject((10,75,200), pygame.Rect(random.randint(25,775), 50, 25,25),random.randint(5,7),3)
    activePowerUps.append(powerUp)

def updateFallingObject(gameObject: GameObject):
    if gameObject.rect.top == 50:
        rand = random.randint(0,1) 
        if rand == 0:
            gameObject.dir = -1
        else:
            gameObject.dir = 1
        
    gameObject.rect = gameObject.rect.move(gameObject.dir*gameObject.vel, gameObject.vel)
        
    # detect if object hits a side wall
    if gameObject.dir == 1 and gameObject.rect.x >= BOARD_WIDTH-gameObject.rect.width:
        gameObject.dir = gameObject.dir * -1  
    elif gameObject.dir == -1 and gameObject.rect.x <= 0+gameObject.rect.width:
        gameObject.dir = gameObject.dir * -1
    pygame.draw.rect(win, gameObject.color, gameObject.rect)
    return gameObject.dead

timers = []
rt = RepeatedTimer(germRNot, addGerm)
rpt = RepeatedTimer(powerUpSpread, addPowerUp)
addGerm()
level = 1

 
  
# Indicates pygame is running
run = True
  
# infinite loop 
while run:
    # creates time delay of 10ms 
    pygame.time.delay(10)
      
    # iterate over the list of Event objects  
    # that was returned by pygame.event.get() method.  
    for event in pygame.event.get():
        
        # if event object type is QUIT  
        # then quitting the pygame  
        # and program both.  
        if event.type == pygame.QUIT:              
            # it will make exit the while loop 
            run = False
    # stores keys pressed 
    keys = pygame.key.get_pressed()
      
    # if left arrow key is pressed
    if keys[pygame.K_LEFT] and player.rect.x>0:
          
        # decrement in x co-ordinate
        player.rect = player.rect.move(-1*player.vel,0)
        
          
    # if left arrow key is pressed
    if keys[pygame.K_RIGHT] and player.rect.x<BOARD_WIDTH-player.rect.width:
          
        # increment in x co-ordinate
        player.rect = player.rect.move(player.vel,0)

    win.fill((0, 0, 255))

    # velocity / speed of movement
    scoreString = "Score: {}".format(score)
    text = font.render(scoreString, True, white, blue)
    levelString = "level: {}".format(level)
    text2 = font.render(levelString, True, white, blue )
    liveString = "lives: {}".format(lives)
    text3 = font.render(liveString, True, white, blue )
    # create a rectangular object for the
    # text surface object
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
       
        if (updateFallingObject(germ) == True):
            activeGerms.remove(germ)
        # germ collision detection
        if (germ.dead == False and player.rect.colliderect(germ.rect)):
            score += 1
            if (score % 5 == 0 ):
                level += 1
                player.rect.width = PLAYER_ORIG_WIDTH
                germRNot -= .2 * germRNot
                if germRNot <= 1:
                    germRNot = 1
                rt.stop()
                rt = RepeatedTimer(germRNot, addGerm)
            player.rect.width = player.rect.width-10
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
        if updateFallingObject(powerUp) == True:
            activePowerUps.remove(powerUp)
        if powerUp.dead == False and player.rect.colliderect(powerUp.rect):
            powerUp.dead = True
            lives +=1
        if powerUp.rect.y >= BOARD_HEIGHT-powerUp.rect.height:
            powerUp.dead = True
        

    # completely fill the surface object  
    # with black colour  
    
   
    # drawing object on screen which is rectangle here 
    pygame.draw.rect(win, player.color, player.rect)



    # it refreshes the window
    pygame.display.update() 


# closes the pygame window 
pygame.quit()
rt.stop()
rpt.stop()

exit()


