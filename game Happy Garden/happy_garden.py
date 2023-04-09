# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 19:04:10 2023

@author: Ronald
"""

from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from random import randint
from pgzero.clock import clock
from PIL import Image
from random import randint
import time
import pgzrun

WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

game_over = False
finalized = False
garden_happy = True
fangflower_collision = False

time_elapsed = 0
start_time = time.time()

cow = Actor("cow")
cow.pos = 100, 500

flower_list = []
wilted_list = []
fangflower_list = []

fangflower_vy_list = []
fangflower_vx_list = []


def draw():
    global game_over, time_elapsed, finalized
    if not game_over:
        screen.clear()
        screen.blit("garden-raining", (0,0))
        cow.draw()
        for flower in flower_list:
            flower.draw()
        for fangflower in fangflower_list:
            fangflower.draw()
        time_elapsed = int (time.time() - start_time)
        screen.draw.text("Garden happy for: " + str(time_elapsed) +" seconds",
                         topleft=(10,10), color="black")
    else:
        if not finalized:
            cow.draw()
            screen.draw.text("Garden happy for: " + str(time_elapsed) +" seconds",
                         topleft=(10,10), color="black")
        if not garden_happy:
            screen.draw.text("GARDEN UNHAPPY! GAME OVER!", color="black", topleft=(10,50))
            finalized = True
        else:
            screen.draw.text("FANGFLOWER ATTACK! GAME OVER!", color="black", topleft=(10,50))
            finalized = True
    return

def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")
    return

def add_flowers():
    global game_over
    if not game_over:
        new_flower()
        clock.schedule(add_flowers, 4)
    return

def check_wilt_times():
    global wilted_list, game_over, garden_happy
    if wilted_list:
        for wilted_since in wilted_list:
            if not wilted_since == "happy":
                time_wilted = int(time.time() - wilted_since)
                if time_wilted > 10:
                    garden_happy = False
                    game_over = True
                    break
    return

def wilt_flower():
    global flower_list, wilted_list, game_over
    if not game_over:
        if flower_list:
            rand_flower = randint(0, len(flower_list)-1)
            if flower_list[rand_flower].image == "flower":
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()
        clock.schedule(wilt_flower, 3)
    return

def rain():
    global flower_list, wilted_list
    if flower_list:
        for flower in flower_list:
            if flower.image == "flower-wilt":
                flower.image = "flower"
                wilted_list[flower_list.index(flower)] = "happy"
    clock.schedule(rain, 5)
    return

add_flowers()
wilt_flower()
rain()

def check_flower_collision():
    global cow, flower_list, wilted_list
    index = 0
    for flower in flower_list:
        if flower.colliderect(cow) and flower.image == "flower-wilt":
            flower.image = "flower"
            wilted_list[index] = "happy"
            break
        index += 1
    return

def check_fangflower_collision():
    global cow, fangflower_list, fangflower_collision, game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = "zap"
            game_over = True
            break
    return

def velocity():
    random_dir = randint(0,1)
    random_velocity = randint(2,3)
    if random_dir == 0:
        return -random_velocity
    else:
        return random_velocity

def mutate():
    global flower_list, fangflower_list, fangflower_vx_list, fangflower_vy_list, game_over
    if not game_over and flower_list:
        rand_flower1 = randint(0, len(flower_list) - 1)
        rand_flower2 = randint(0, len(flower_list) - 1)
        while rand_flower2 == rand_flower1: # make sure we're not selecting the same flower twice
            rand_flower2 = randint(0, len(flower_list) - 1)
        fangflower_pos_x1 = flower_list[rand_flower1].x
        fangflower_pos_y1 = flower_list[rand_flower1].y
        fangflower_pos_x2 = flower_list[rand_flower2].x
        fangflower_pos_y2 = flower_list[rand_flower2].y
        del flower_list[rand_flower1]
        if rand_flower1 < rand_flower2:
            del flower_list[rand_flower2 - 1] # remove the second flower first to adjust the index
        else:
            del flower_list[rand_flower2]
        fangflower1 = Actor("fangflower")
        fangflower1.pos = fangflower_pos_x1, fangflower_pos_y1
        fangflower2 = Actor("fangflower")
        fangflower2.pos = fangflower_pos_x2, fangflower_pos_y2
        fangflower_vx1 = velocity()
        fangflower_vy1 = velocity()
        fangflower_vx2 = velocity()
        fangflower_vy2 = velocity()
        fangflower_list.append(fangflower1)
        fangflower_list.append(fangflower2)
        fangflower_vx_list.append(fangflower_vx1)
        fangflower_vy_list.append(fangflower_vy1)
        fangflower_vx_list.append(fangflower_vx2)
        fangflower_vy_list.append(fangflower_vy2)
        clock.schedule(mutate, 20)


def update_fangflowers():
    global fangflower_list, game_over
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx
            fangflower.y += fangflower_vy
            if fangflower.left < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index += 1
    return


def reset_cow():
    global game_over
    if not game_over:
        cow.image = "cow"
    return

add_flowers()
wilt_flower()


def update():
    global score, game_over, fangflower_collision, flower_list, fangflower_list, time_elapsed
    fangflower_collision = check_fangflower_collision()
    check_wilt_times()
    if not game_over:
        if keyboard.space:
            cow.image = "cow-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
        elif keyboard.up and cow.y > 150:
            cow.y -= 5
        elif keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        if time_elapsed > 15 and not fangflower_list:
            mutate()
            
        update_fangflowers()


pgzrun.go()
