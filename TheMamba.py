import sys
import pygame
from time import time, sleep
from random import randint
from win32api import GetSystemMetrics
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = str(0) + "," + str(0)

window = [GetSystemMetrics(0), GetSystemMetrics(1)]

color = [255,255,255]
red = [255,0,0]
blue = [0,0,255]
green = [0,255,0]
screen = pygame.display.set_mode(window)
DISPLAY = pygame.Surface(window)

class ScoreBoard:
    def __init__(self):
        self.score = 0
    def showScore(self):
        pygame.font.init()  # you have to call this at the start,
        scorefont = pygame.font.SysFont('Arial', 20)
        scoreDisplay = scorefont.render("Score: " + str(self.score), False, (0, 0, 0))
        screen.blit(scoreDisplay, (window[0]-100,0))

class Apple:
    def __init__(self):
        self.position = []
    def showApple(self):
        pygame.draw.rect(DISPLAY, blue, (self.position[0], self.position[1], 10, 10))
        screen.blit(DISPLAY,(0,0))

class SnakeSegment:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed

class Snake:
    def __init__(self):
        self.headCoord = []
        self.segments = []
        self.tailSegment = []
        self.headCoord.append(window[0]/2)
        self.headCoord.append(window[1]/2)
        self.segments.append(SnakeSegment(self.headCoord, [1,0]))
        self.tailSegment = self.segments[len(self.segments)-1]

    def addSegment(self):
        self.segments = self.segments + [SnakeSegment([self.segments[len(self.segments)-1].position[0] - 10*self.segments[len(self.segments)-1].speed[0] , \
                                           self.segments[len(self.segments) - 1].position[1] - 10*self.segments[len(self.segments)-1].speed[1]], \
                                          self.segments[len(self.segments) - 1].speed)]

    def move(self, dir, apple):
        game_over = False
        appleEaten = False
        newSegment = SnakeSegment([self.segments[0].position[0]+10*dir[0], self.segments[0].position[1]+10*dir[1]],self.segments[0].speed)
        newSegment.position[0] = newSegment.position[0]
        newSegment.position[1] = newSegment.position[1]
        self.segments = [newSegment] + self.segments
        if self.isIntersecting():
            game_over = True
        if apple.position[0] != newSegment.position[0] or apple.position[1] != newSegment.position[1]:
            del self.segments[len(self.segments)-1]
        else:
            appleEaten = True

        if self.segments[0].position[0] > window[0]:
            game_over = True
            self.segments[0].position[0] = 0
        if self.segments[0].position[0] < 0:
            game_over = True
            self.segments[0].position[0] = window[0]

        if self.segments[0].position[1] > window[1]:
            game_over = True
            self.segments[0].position[1] = 0
        if self.segments[0].position[1] < 0:
            game_over = True
            self.segments[0].position[1] = window[1]

        return game_over,appleEaten

    def isIntersecting(self):
        for x in range(1, len(self.segments)):
            if self.segments[0].position[0]==self.segments[x].position[0] \
                    and \
               self.segments[0].position[1]==self.segments[x].position[1]:
                return True
        return False


    def showSnake(self):
        for x in range(0, len(self.segments)):
            pygame.draw.rect(DISPLAY, red, (self.segments[x].position[0],self.segments[x].position[1],10,10))
        screen.blit(DISPLAY,(0,0))

mySnake = Snake()
myApple = Apple()
myScore = ScoreBoard()
speed = [round(1),round(0)]
myApple.position = [randint(10,190),randint(10,190)]
myApple.position[0] = myApple.position[0] - myApple.position[0]%10
myApple.position[1] = myApple.position[1] - myApple.position[1]%10

direction = [1,0]
game_over = False; apple_eaten = False

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            print len(mySnake.segments)
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_LEFT:
                if direction[0]==0:
                    direction = [-1,0]
            if event.key == pygame.K_RIGHT:
                if direction[0]==0:
                    direction = [1, 0]
            if event.key == pygame.K_UP:
                if direction[1]==0:
                    direction = [0, -1]
            if event.key == pygame.K_DOWN:
                if direction[1]==0:
                    direction = [0, 1]

    DISPLAY.fill(color)

    mySnake.showSnake()
    myApple.showApple()
    myScore.showScore()

    game_over, apple_eaten = mySnake.move(direction, myApple)

    if game_over:
        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        myfont = pygame.font.SysFont('Arial', 50)
        DISPLAY = myfont.render('Game Over!', False, (0, 0, 0))
        screen.blit(DISPLAY, (window[0]/2 - 100, window[1]/2 -50))

    else:
        if apple_eaten:
            myScore.score = myScore.score + 10
            myApple.position = [randint(10, 190), randint(10, 190)]
            myApple.position[0] = myApple.position[0] - myApple.position[0] % 10
            myApple.position[1] = myApple.position[1] - myApple.position[1] % 10
            myApple.showApple()
            myScore.showScore()
        sleep(0.1)

    pygame.display.flip()

