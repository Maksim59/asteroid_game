# Maksim Isayenka
# 2024-04-11
# isayenka_maksim_asteroid_game.py
# This is my asteroid game

import pygame  # make everything available to us
import random  # needed for generating sudo-random number
import time    # needed to make pauses on screens

pygame.init()  # initialize the module

# screen size
ScreenW = 1100  # make variables for width and height
ScreenH = 700

bolRun = True  # this will be the infinite loop

screen = pygame.display.set_mode((ScreenW, ScreenH))

#Create my images
bgImg = pygame.image.load('images/bg.jpeg').convert_alpha()
bgImg = pygame.transform.scale(bgImg, (ScreenW,ScreenH))

endImg = pygame.image.load('images/end.png').convert_alpha()
endImg = pygame.transform.scale(endImg, (ScreenW,ScreenH))

pauseImg = pygame.image.load('images/pause.png')
pauseImg = pygame.transform.scale(pauseImg, (ScreenW, ScreenH))

startImg = pygame.image.load('images/start.png')

font = pygame.font.Font("freesansbold.ttf", 32)
text = font.render("Asteroids", True, (0,255,0))

pygame.display.set_caption("Asteroids")

shipImg = pygame.image.load('images/Ship1.png').convert_alpha()
shipImg = pygame.transform.scale(shipImg,(50,50))

full = pygame.image.load('images/last.png').convert_alpha()
full = pygame.transform.scale(full, (75,75))

mid = pygame.image.load('images/mid.png').convert_alpha()
mid = pygame.transform.scale(mid, (75,75))

first = pygame.image.load('images/first.png').convert_alpha()
first = pygame.transform.scale(first, (75,75))

astImg = pygame.image.load('images/ASTEROID.png').convert_alpha()
astImg = pygame.transform.scale(astImg, (100,100))

MisImg = pygame.image.load('images/missle.png').convert_alpha()
MisImg = pygame.transform.scale(MisImg, (50,30))

splitAstImg = pygame.transform.scale(astImg, (25,25))

ASTEROID = []  # create an empty list called wall
missle = [] # create a list to store missles
astScore = 0
lives = 3
xC = 0

# ************** CLASSES ********************
class clsASTEROID():
    """
    Creates a class for an asteroid that uses multiple parameters including x-location, y-location, x-direction,
    y-direction, image
    """
    def __init__(self, Xloc, Yloc, DirX, DirY, Image):
        self.Xloc = Xloc  # top location
        self.Yloc = Yloc  # left location
        self.DirX = DirX  # direction of movement in X axis
        self.DirY = DirY  # direction of movement in Y axis
        self.width = 40
        self.height = 40
        self.speed = 1
        self.active = True
        self.color = (255, 0, 255)
        self.Image = Image

class clsMissle():
    """
    Creates a missle class that takes in parameters for x-location, y-location, missle angle
    """
    def __init__(self, Xloc, Yloc, Angle):
        self.Xloc = Xloc
        self.Yloc = Yloc
        self.DirX = 1
        self.DirY = 1
        self.speed = 5
        self.active = False
        self.Angle = Angle
        self.Image = MisImg
        self.ammo = 0
class clsShip():
    """
    Creates a class for a ship that uses paramaters for x-location, y-location, and image
    """
    def __init__(self, Xloc, Yloc, Image):
        self.Xloc = Xloc
        self.Yloc = Yloc
        self.Dir = 0  # might not need
        self.width = 50
        self.height = 50
        self.Speed = 1
        self.image = Image
        self.Angle = 0
        self.active = True

def funStart():
    #Creates a function that creates a starting screen to explain the keybinds
    screen.blit(startImg, (0,0))
    font = pygame.font.Font("freesansbold.ttf", 50)
    text = font.render("Press <g> to pause", True, (255, 255, 255))
    screen.blit(text, (300, 500))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return False

ship = clsShip(500,500, shipImg) # creates a ship instance
speed = ship.Speed
# ************** FUNCTIONS ********************
def rot_center(image, angle):
    # creates a function to rotate a ship without distorting it
    orig_rect = image.get_rect()
    ship.Angle = ship.Angle + angle
    rot_image = pygame.transform.rotate(image, ship.Angle)
    if ship.Angle >=360: ship.Angle = 0
    if ship.Angle ==-45: ship.Angle = 315 # correct negative directions
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def funSHOOT():
    #creats a function that shoots the missle
    global xC
    missle[xC].Angle = ship.Angle
    missle[xC].Xloc = ship.Xloc
    missle[xC].Yloc = ship.Yloc
    missle[xC].active = True
    xC += 1
    if xC >= 10:
        xC = 0

def funPause():
    #creates a function that pauses the screen
    while True:
        screen.blit(pauseImg, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return False
def funKEYS():  # check for keyboard and mouse input
    global bolRun  # so there is only one version out there
    # check for keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pressed the close X on window
            bolRun = False
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                #rotate left
                ship.image = rot_center(shipImg,45)
            elif event.key == pygame.K_s:
                #rotate_right
                ship.image = rot_center(shipImg, -45)
            elif event.key == pygame.K_t and ship.active:
                #increase speed while the ship is active, max speed is 3
                if ship.Speed < 3:
                    ship.Speed += 1
            elif event.key == pygame.K_y:
                #decrease speed while the ship is active, min speed is 1
                if ship.Speed > 1 and ship.active:
                    ship.Speed -= 1
            elif event.key == pygame.K_o:
                #respawns the ship in the center
                if ship.active == False:
                    funRespawn()
            elif event.key == pygame.K_g:
                #pauses the game
                funPause()
            elif event.key == pygame.K_l:
                #shoots the missle
                if ship.active == True:
                    funSHOOT()

    keys = pygame.key.get_pressed()  # check what was pressed
    if keys[pygame.K_SPACE]:
        #Make the ship move by clicking space and make it so that it moves in the direction its angled at
        if ship.Angle == 0:
            ship.Yloc = ship.Yloc - (ship.Speed)
        elif ship.Angle == 45:
            ship.Xloc = ship.Xloc - (ship.Speed)
            ship.Yloc = ship.Yloc - (ship.Speed)
        elif ship.Angle == 90:
            ship.Xloc = ship.Xloc - (ship.Speed)
        elif ship.Angle == 135:
            ship.Xloc = ship.Xloc - (ship.Speed)
            ship.Yloc = ship.Yloc + (ship.Speed)
        elif ship.Angle == 180:
            ship.Yloc = ship.Yloc + (ship.Speed)
        elif ship.Angle == 225:
            ship.Xloc = ship.Xloc + (ship.Speed)
            ship.Yloc = ship.Yloc + (ship.Speed)
        elif ship.Angle == 270:
            ship.Xloc = ship.Xloc + (ship.Speed)
        elif ship.Angle == 315:
            ship.Xloc = ship.Xloc + (ship.Speed)
            ship.Yloc = ship.Yloc - (ship.Speed)

def funCOLIDE():  # collision checking between ASTEROID and Ship
    global lives
    global astScore
    if ship.active:
        ship_HB = ship.image.get_rect(topleft = (ship.Xloc, ship.Yloc)) #creates a hitbox for the ship
        for i in range(len(ASTEROID)):
            if ASTEROID[i].active == True: #makes sure everything is done while the asteroid is active
                if ASTEROID[i].Image == splitAstImg: # checks if the asteroid is a small one
                    ASTEROID[i].speed = 2 #makes the small asteroid fast
                    ASTEROID_rect = pygame.Rect(ASTEROID[i].Xloc, ASTEROID[i].Yloc, 25, 25) #creates a smaller hitbox around the asteroid
                else:
                    ASTEROID_rect = pygame.Rect(ASTEROID[i].Xloc, ASTEROID[i].Yloc, ASTEROID[i].width,ASTEROID[i].height) #creates a regular hitbox on the asteroid
                if ship_HB.colliderect(ASTEROID_rect):
                    #checks if the ship colides with the asteroid and makes the ship not active and decreases the amount of lives by 1
                    ship.active = False
                    lives -= 1

                for j in range(len(missle)):
                    if missle[j].active == True:
                        #checks if the missle is active
                        missle_HB = missle[j].Image.get_rect(topleft=(missle[j].Xloc, missle[j].Yloc)) #creates a hitbox around the missle
                        if ASTEROID_rect.colliderect(missle_HB):
                            #checks if the asteroid and the ship is colided and then makes the asteroid not active
                            ASTEROID[i].active = False
                            if ASTEROID[i].Image == astImg:
                                #checks if the image is the regular image and then creates two instances of the asteroids where it
                                #creates one asteroid that goes the opposite way by multiplying the directions by -1 and then another
                                #asteroid that goes the same way and just keeping the directions the same
                                ASTEROID.append(clsASTEROID(ASTEROID[i].Xloc, ASTEROID[i].Yloc, ASTEROID[i].DirX * -1, ASTEROID[i].DirY * -1, splitAstImg))
                                ASTEROID.append(clsASTEROID(ASTEROID[i].Xloc, ASTEROID[i].Yloc, ASTEROID[i].DirX, ASTEROID[i].DirY, splitAstImg))

                            RndX = int(random.randint(50, 800))
                            RndY = int(random.randint(0, 1))
                            RndDirX = random.randint(-1, 1)
                            RndDirY = 1

                            if(len(ASTEROID) % 3 == 0):
                                #A way I came up with to keep the asteroids spawning and if the number is divisible by 3 it spawns
                                ASTEROID.append(clsASTEROID(RndX, RndY, RndDirX, RndDirY, astImg))
                            if ASTEROID[i].Image == astImg:
                                #adds 50 to the score if the asteroid is a big one
                                astScore += 50
                            if ASTEROID[i].Image == splitAstImg:
                                #adds 100 to the score if the asteroid is a small image
                                astScore += 100
                            missle[j].active = False


def funMOVE():  # calculate the movement of ojects controlled by computer
    for i in range(len(ASTEROID)):
        #Makes it so that the asteroid can cross between the screen so if it goes through one wall it comes throught
        #the opposite one
        if ASTEROID[i].Xloc>= ScreenW:
            ASTEROID[i].Xloc = 0
        elif ASTEROID[i].Xloc <= 0-ASTEROID[i].width:
            ASTEROID[i].Xloc = ScreenW
        if ASTEROID[i].Yloc >= ScreenH:
            ASTEROID[i].Yloc = 0
        elif ASTEROID[i].Yloc <= 0-ASTEROID[i].height:
            ASTEROID[i].Yloc = ScreenH

        ASTEROID[i].Xloc = ASTEROID[i].Xloc + (ASTEROID[i].DirX * ASTEROID[i].speed)
        ASTEROID[i].Yloc = ASTEROID[i].Yloc + (ASTEROID[i].DirY * ASTEROID[i].speed)

    #makes it so that the ship can cross between walls and a for loop is not needed because we have one instance of the ship
    if ship.Xloc >= ScreenW:
        ship.Xloc = 0
    elif ship.Xloc <= 0 - ASTEROID[i].width:
        ship.Xloc = ScreenW
    if ship.Yloc >= ScreenH:
        ship.Yloc = 0
    elif ship.Yloc <= 0 - ship.height:
        ship.Yloc = ScreenH


    for i in range(len(missle)):
        #loops through the length of the missle list and makes it so that the missle's angle matches the ship angle
        if missle[i].Angle == 0:
            missle[i].Yloc = missle[i].Yloc - missle[i].speed
        elif missle[i].Angle == 45:
            missle[i].Xloc = missle[i].Xloc - missle[i].speed
            missle[i].Yloc = missle[i].Yloc - missle[i].speed
        elif missle[i].Angle == 90:
            missle[i].Xloc = missle[i].Xloc - missle[i].speed
        elif missle[i].Angle == 135:
            missle[i].Xloc = missle[i].Xloc - missle[i].speed
            missle[i].Yloc = missle[i].Yloc + missle[i].speed
        elif missle[i].Angle == 180:
            missle[i].Yloc = missle[i].Yloc + missle[i].speed
        elif missle[i].Angle == 225:
            missle[i].Xloc = missle[i].Xloc + missle[i].speed
            missle[i].Yloc = missle[i].Yloc + missle[i].speed
        elif missle[i].Angle == 270:
            missle[i].Xloc = missle[i].Xloc + missle[i].speed
        elif missle[i].Angle == 315:
            missle[i].Xloc = missle[i].Xloc + missle[i].speed
            missle[i].Yloc = missle[i].Yloc - missle[i].speed

def funEnd():
    #creates a function that shows a game over screen
    screen.blit(endImg, (0,0))
    pygame.display.update()

def funDRAW():  # redraw the screen and all objects
    screen.fill((0, 0, 0))  # "fill" the screen object with RGB color
    screen.blit(bgImg, (0, 0))
    for i in range(len(missle)):
        if missle[i].active == True:
            screen.blit(MisImg, (missle[i].Xloc,missle[i].Yloc))
    if(ship.active):
        screen.blit(ship.image, (ship.Xloc,ship.Yloc))

    # draw the ASTEROID object
    for i in range(len(ASTEROID)):
        if ASTEROID[i].active:
            screen.blit(ASTEROID[i].Image, (ASTEROID[i].Xloc, ASTEROID[i].Yloc))
    screen.blit(text, (450,10))
    global astScore
    scoreFont = pygame.font.Font("freesansbold.ttf", 32)
    scoreText = scoreFont.render("Score: " + str(astScore), True, (0, 255, 0))
    if astScore > 2000:
        #makes it so that if the score is greater than 2000 the colour of the score is red
        scoreText = scoreFont.render("Score: " + str(astScore), True, (255, 0, 0))
    if astScore > 5000:
        #makes it so that if the score is greater than 5000 the colour of the score is gold
        scoreText = scoreFont.render("Score: " + str(astScore), True, (255, 215, 0))
    screen.blit(scoreText, (20, 20))
    livesText = scoreFont.render("Lives: " + str(lives), True, (0, 255, 0))
    speedText = scoreFont.render("Speed: " + str(ship.Speed), True, (0, 255, 0))
    screen.blit(livesText, (20,50))
    screen.blit(speedText, (850, 80))

    if ship.Speed == 1:
        #makes it so that the first image of the speedometer shows if the speed is 1
        screen.blit(first, (910, 10))
    if ship.Speed == 2:
        #makes it so that the middle image of the speedometer shows if the speed is 2
        screen.blit(mid, (910, 10))
    if ship.Speed == 3:
        #makes it so that the full image of the speedometer shows if the speed is 3
        screen.blit(full, (910,10))
    pygame.display.update()  # actually draw the updated screen

def funRespawn():
    #creates a function that respawns the ship
    ship.active = True
    ship.Xloc = 500
    ship.Yloc = 300

# ************** RUN ONLY ONCE ********************

def funCreateAsteroids():
    #creates a function that creates asteroids
    for i in range(6):
        RndX = int(random.randint(50, 800))
        RndY = int(random.randint(50, 80))
        RndDirX = random.randint(-1, 1)
        RndDirY = random.randint(-1, 1)

        if RndDirY == 0 and RndDirX == 0:
            RndDirY = 1
            RndDirX = 1

        ASTEROID.append(clsASTEROID(RndX, RndY, RndDirX, RndDirY, astImg))  # create an instance of clsASTEROID with those values

for i in range(10):
    #creates a bunch of instances of the missle
    missle.append(clsMissle(ship.Xloc, ship.Yloc, ship.Angle))
# **************************** MAIN PROGRAM LOOP *****************

#while loop so that while no key is pressed it blits an image of the start screen

while True:
    starting = funStart()
    if starting == False:
        break

funCreateAsteroids()
while bolRun:
    funKEYS()  # check keyboard/mouse
    funMOVE()  # move the ASTEROID
    if(funCOLIDE()):  # check for collision
        ship.active = True
    funDRAW()  # redraw the entire screen
    pygame.time.delay(5)
    if lives == 0:
        #if there are no more lives it calls the ending function and waits 5 seconds before it quits
        funEnd()
        time.sleep(5)
        pygame.quit()
    # we will need this to actually smooth things out a bit

# ************** CLEANUP and EXIT ********************

print("Thanks for playing...")



