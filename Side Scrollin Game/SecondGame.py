import pygame
import SecondGameClasses
from SecondGameClasses import player
from SecondGameClasses import spike
from SecondGameClasses import saw
from pygame.locals import *
import os
import sys
import math
import random

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()

clock = pygame.time.Clock()

pygame.time.set_timer(USEREVENT+1, 500)
pygame.time.set_timer(USEREVENT+2, random.randrange(3500, 5000))
speed = 30
run = True

runner = player(200, 313, 64, 64)
spikee = spike(300, 0, 48, 320)
saww = saw(300, 300, 64, 64)


def reDrawGameWindow():
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    for object in objects:
        object.draw(win)
    font = pygame.font.SysFont(("comicsans"), 30)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (375, 10))
    pygame.display.update()


def updateFile():
    f = open("scores.txt", "r")
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open("scores.txt", "w")
        file.write(str(score))
        file.close()

        return score
    return last


def endScreen():
    global pause, objects, speed, score
    pause = 0
    objects = []
    speed = 30
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
        win.blit(bg, (0, 0))
        largeFont = pygame.font.SysFont(("comicsans"), 80)
        previousScore = largeFont.render("previous Score: " + str(updateFile()), 1, (255, 255, 255))
        win.blit(previousScore, (W/2 - previousScore.get_width()/2, 200))
        newScore = largeFont.render("Score: " + str(score), 1, (255, 255, 255))
        win.blit(newScore, (W/2 - newScore.get_width()/2, 320))
        pygame.display.update()
    score = 0
    runner.falling = False


pause = 0
fallSpeed = 0
objects = []
while run:
    score = speed // 5 - 6
    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            endScreen()
    for objectt in objects:
        if objectt.collide(runner.hitbox):
            runner.falling = True
            if pause == 0:
                fallSpeed = speed
                pause = 1

        objectt.x -= 1.4
        if objectt.x < -objectt.width * -1:
            objects.pop(objects.index(objectt))

    clock.tick(speed)
    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
            speed += 1
        if event.type == USEREVENT+2:
            r = random.randrange(0, 2)
            if r == 0:
                objects.append(saw(810, 310, 64, 64))
            else:
                objects.append(spike(810, 0, 48, 320))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
        if not(runner.jumping):
            runner.jumping = True
    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            runner.sliding = True
    reDrawGameWindow()
