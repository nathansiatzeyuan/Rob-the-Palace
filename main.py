import pygame
import random
import math
from PIL import Image

pygame.init()
screen_length = 1300
screen_width = 800
screen = pygame.display.set_mode((screen_length, screen_width))
iconIMG = pygame.image.load("thief.png")
pygame.display.set_icon(iconIMG)
pygame.display.set_caption("Rob the Palace")
wallIMG = pygame.image.load("wall.png")
bgIMG = pygame.image.load("black bg.jpg")

# Wall
wallX = 0
wallY = 0
no_of_walls = math.ceil(screen_length / 64)


def wall(x):
    if x <= screen_length:
        for i in range(no_of_walls):
            screen.blit(wallIMG, (x, 0))
            screen.blit(wallIMG, (x, screen_width - 64))
            x += 64


# Robber
robberIMG = pygame.image.load("thief (1).png")
robberX = 600
robberY = screen_width - 128
robberX_change = 0
robberY_change = 0
robberY_maxpoint = 64
robberY_minpoint = screen_width - 128
robberX_maxpoint = screen_length - 64


def robber(x, y):
    screen.blit(robberIMG, (x, y))


# Background Image
def background(x, y):
    screen.blit(bgIMG, (x, y))


# Direction of Robber
looking_right = True
non_inverted = True

# Coin
coin_non_inverted = True
coinIMG = pygame.image.load("treasure-chest.png")
coinX = random.randint(0, 1236)
coinY = random.choice([robberY_maxpoint, robberY_minpoint])
if coinY == robberY_maxpoint:
    coinIMG = pygame.transform.flip(coinIMG, False, True)


def coin(x, y):
    screen.blit(coinIMG, (x, y))


# Score and scoreboard
score = 0
font = pygame.font.Font('mariotext.ttf', 25)
scoreboardX = 0
scoreboardY = 64


def scoreboard(x, y):
    scoreboard1 = font.render("Score " + str(score), True, (255, 255, 255))
    screen.blit(scoreboard1, (x, y))


# Collision between Coin and Robber

def iscollision(x1, x2, y1, y2):
    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if d < 50:
        return True
    else:
        return False
    score += 10


# Rocket
no_of_rockets=10
rocketIMG=[]
rocketleftIMG=[]
rocketrightIMG=[]
rocketX=[]
rocketY=[]
rocket_direction=[]
rocketX_change=[]
for i in range(no_of_rockets):
    rocketIMG.append( pygame.image.load("rocket.png"))
    rocketleftIMG .append (pygame.transform.rotate(rocketIMG[i], -90))
    rocketrightIMG .append( pygame.transform.rotate(rocketIMG[i], 90))
    rocketX .append(random.choice([0, screen_length - 64]))
    rocketY .append(random.randint(64, screen_width - 128))
    rocket_direction.append( "undefined")
    rocketX_change.append (2)


def rocket(x, y,i):
    global rocket_direction
    if x == 0 and rocket_direction[i] == "undefined":
        screen.blit(rocketleftIMG[i], (x, y))
        rocket_direction[i] = "right"
    if rocket_direction[i] == "right":
        screen.blit(rocketleftIMG[i], (x, y))


    if x == screen_length - 64 and rocket_direction[i] == "undefined":
        screen.blit(rocketrightIMG[i], (x, y))
        rocket_direction[i] = "left"
    if rocket_direction[i] == "left":
        screen.blit(rocketrightIMG[i], (x, y))

#Collision between rocket and robber
def collision_btw_rkt_and_robber(x1, x2, y1, y2):
    d = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    if d < 20:
        return True
collide=False

#GameOver
font1 = pygame.font.Font('mariotext.ttf', 100)
gameoverX = 520
gameoverY = screen_width/2

def gameover(x, y):
    gameover1 = font.render("GAME OVER ", True, (255, 255, 255))
    screen.blit(gameover1, (x, y))
running = True
while running:
    background(0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # PRESSING KEY
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                robberX_change = -1.5
                if looking_right:
                    robberIMG = pygame.transform.flip(robberIMG, True, False)
                    looking_right = False

            if event.key == pygame.K_RIGHT:
                robberX_change = 1.5
                if not looking_right:
                    robberIMG = pygame.transform.flip(robberIMG, True, False)
                    looking_right = True

            if event.key == pygame.K_UP:
                robberY_change = -1.5
                if non_inverted:
                    robberIMG = pygame.transform.flip(robberIMG, False, True)
                    non_inverted = False

            if event.key == pygame.K_DOWN:
                robberY_change = 1.5
                if not non_inverted:
                    robberIMG = pygame.transform.flip(robberIMG, False, True)
                    non_inverted = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP:
                robberX_change = 0

        # Robber
    if robberY < robberY_maxpoint:
        robberY = robberY_maxpoint
    if robberY > robberY_minpoint:
        robberY = robberY_minpoint

    # Boundaries
    if robberX < 0:
        robberX = 0
    elif robberX > robberX_maxpoint:
        robberX = robberX_maxpoint

    robberX += robberX_change
    robberY += robberY_change

    # Collision between robber and coin
    collision_btw_robber_coin = iscollision(coinX, robberX, coinY, robberY)
    if collision_btw_robber_coin and coinY == robberY_minpoint:
        coinX = random.randint(0, 1236)
        coinY = random.choice([robberY_maxpoint, robberY_minpoint])
        if coinY == robberY_maxpoint:
            coinIMG = pygame.transform.flip(coinIMG, False, True)
        score += 10

    if collision_btw_robber_coin and coinY == robberY_maxpoint:
        coinX = random.randint(0, 1236)
        coinY = random.choice([robberY_maxpoint, robberY_minpoint])
        if coinY == robberY_minpoint:
            coinIMG = pygame.transform.flip(coinIMG, False, True)
        score += 10

    # Rocket
    for i in range (no_of_rockets):
        rocket(rocketX[i], rocketY[i],i)
        if rocket_direction[i] == "right":
            rocketX[i] += rocketX_change[i]
        if rocket_direction[i] == "left":
            rocketX[i] += (-rocketX_change[i])

        # Reload the rocket when the rocket hit the boudnaries
        if (rocket_direction[i] == "right" and rocketX[i] == screen_length) or (rocket_direction[i] == "left" and rocketX[i]==0):
            rocket_direction[i] = "undefined"
            rocketX[i] = random.choice([0, screen_length - 64])
            rocketY[i] = random.randint(64, screen_width - 128)

        #Collision between robber and rocket
        collision_between_rkt_and_robber=collision_btw_rkt_and_robber(robberX, rocketX[i], robberY, rocketY[i])
        if collision_between_rkt_and_robber:
            collide=True
        if collide==True:
            gameover(gameoverX,gameoverY)
            break


    robber(robberX, robberY)
    wall(0)
    coin(coinX, coinY)
    scoreboard(scoreboardX, scoreboardY)

    pygame.display.update()
