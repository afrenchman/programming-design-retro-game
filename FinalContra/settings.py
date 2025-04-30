import os
import pygame

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
DARK_GREEN = (2,207,16)
BLUE = (0,0,255)
SEA_BLUE = (0,86,255)
LIGHT_YELLOW = (255,251,168)
YELLOW = (255,255,0)
DARK_YELLOW = (255,150,2)

# Project Properties
TITLE = "Contra"
WIDTH = 1920
HEIGHT = 1080
windowSize = (WIDTH,HEIGHT)
FPS = 60


# Camera

LEFT_BOUND = 0
RIGHT_BOUND = -13869

# Assets folder
gameFolder = os.path.dirname(__file__)
imgFolder = os.path.join(gameFolder,"img")
soundFolder = os.path.join(gameFolder,"sounds")


# Player

PLAYER_HEALTH = 10
PLAYER_POSX = 300
PLAYER_ACC = 0.65
PLAYER_FRC = -0.12
PLAYER_WIDTH = 78
PLAYER_HEIGHT = 123
GRAVITY = 1
JUMP_HEIGHT = 25
BLINK_TIME = 10
BLINK_DISTANCE = 300
BLINK_SPEED = 20
BLINK_RETRACT = 500
ANIM_SPEED = 5

# Powerups
POWERUP_SPEED = 10
POWERUP_TIME = 300

# Bullet

BULLET_SPEED = 10
BULLET_THRESHOLD = 50

# Sniper
SNIPER_RANGE = 500

LEVEL_1_SNIPERS = [(1149, 643), (1563, 657), (3246, 364), (6079, 225), (6225, 776),
                   (7087, 490), (9328, 564), (10467, 344), (11722, 546), (12847, 774),
                   (14555, 639)]

# Soldier
SOLDIER_SPEEDX = 13
SOLDIER_SPEEDY = 0
SOLDIER_SPAWN_TIMER = 120

LEVEL_1_SOLDIERS = [(1125, 22)]

# Tank
TANK_WIDTH = 100
TANK_HEIGHT = 60


LEVEL_1_TANKS = [(8145, 267), (7857, 549), (11283, 668), (12622, 519),
                 (13234, 679), (14256, 819), (14235, 400)]

#platforms
PLATFORM_THICKNESS = 1
pt = PLATFORM_THICKNESS

#LEVEL_1
LEVEL_1 = [
    (-1050,HEIGHT-pt,WIDTH*20,pt), (1282, 915, 247, pt), (1125, 765, 123, pt),
    (1552, 765, 123, pt), (702, 636, 405, pt), (139, 488, 3217, pt),
    (1831, 630, 247, pt), (2686, 909, 247, pt), (2823, 704, 393, pt),
    (3971, 501, 675, pt), (5220, 501, 1102, pt), (6221, 922, 393, pt),
    (6070, 348, 2241, pt), (6637, 720, 263, pt), (7067, 607, 922, pt),
    (7625, 913, 832, pt), (8282, 490, 877, pt), (8471, 776, 270, pt),
    (8892, 774, 270, pt), (9029, 344, 697, pt), (9315, 702, 123, pt),
    (9594, 630, 405, pt), (9877, 490, 270, pt), (10293, 911, 27, pt),
    (10293, 625, 270, pt), (10437, 486, 270, pt), (10865, 911, 123, pt),
    (10863, 623, 270, pt), (11004, 771, 405, pt), (11432, 490, 270, pt),
    (11571, 913, 123, pt), (11569, 348, 270, pt), (11713, 702, 123, pt),
    (11997, 490, 270, pt), (12132, 632, 697, pt), (12559, 918, 405, pt),
    (13122, 774, 270, pt), (13545, 632, 270, pt), (13828, 490, 540, pt),
    (13828, 913, 900, pt), (13968, 702, 405, pt), (14391, 630, 123, pt),
    (14535, 769, 123, pt)
]
LEVEL_1_BG = 'l1.png'

LEVEL_1_PUPS = [(4293, 6)]

LEVEL_1_BOSSES = [(14886, 186), (14980, 384), (14886, 580), (14980, 792)]

