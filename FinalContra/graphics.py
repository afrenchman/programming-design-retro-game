import pygame
from settings import *
import os


class SpriteSheet(object):

    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)

        scale_factor = 2.25
        scaled_width = int(width * scale_factor)
        scaled_height = int(height * scale_factor)
        image = pygame.transform.scale(image, (scaled_width, scaled_height))

        return image

# Load graphics ##############################################

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode(windowSize)

# Start Screen Background ####################################

ss_background = pygame.image.load(os.path.join(imgFolder,'start.jpg')).convert()

# Background image ###########################################

l1_bg = pygame.image.load(os.path.join(imgFolder,'l1.png')).convert()

# Bullet images ##############################################

bulletImage = pygame.image.load(os.path.join(imgFolder,'bullet.png')).convert()

# Game Over ##################################################

game_over = pygame.image.load(os.path.join(imgFolder,'game_over.png')).convert()

# Mob images #################################################

soldier_sheet = SpriteSheet(os.path.join(imgFolder,'enemies.png'))

##############################################################

player_sheet = SpriteSheet(os.path.join(imgFolder,'playersheet.png'))

PLAYER_RIGHT_0 = player_sheet.get_image(326, 33, 56, 83).convert()
PLAYER_RIGHT_1 = player_sheet.get_image(324, 299, 49, 81).convert()
PLAYER_RIGHT_2 = player_sheet.get_image(376, 301, 49, 81).convert()
PLAYER_RIGHT_3 = PLAYER_RIGHT_0
PLAYER_RIGHT_4 = player_sheet.get_image(427, 303, 54, 78).convert()
PLAYER_RIGHT_5 = player_sheet.get_image(490, 299, 42, 78).convert()
PLAYER_RIGHT_6 = player_sheet.get_image(544, 297, 40, 83).convert()

PLAYER_RIGHT_UP_0 = player_sheet.get_image(326, 213, 45, 78).convert()
PLAYER_RIGHT_UP_1 = player_sheet.get_image(384, 213, 51, 74).convert()
PLAYER_RIGHT_UP_2 = player_sheet.get_image(448, 216, 56, 76).convert()

PLAYER_RIGHT_DOWN_0 = player_sheet.get_image(324, 123, 42, 81).convert()
PLAYER_RIGHT_DOWN_1 = player_sheet.get_image(382, 126, 42, 78).convert()
PLAYER_RIGHT_DOWN_2 = player_sheet.get_image(438, 126, 51, 78).convert()

PLAYER_JUMP_0 = player_sheet.get_image(411, 396, 49, 38).convert()
PLAYER_JUMP_1 = player_sheet.get_image(463, 384, 38, 45).convert()
PLAYER_JUMP_2 = player_sheet.get_image(506, 393, 49, 38).convert()
PLAYER_JUMP_3 = player_sheet.get_image(560, 387, 38, 45).convert()

PLAYER_DEAD_0 = player_sheet.get_image(324, 445, 56, 42).convert()
PLAYER_DEAD_1 = player_sheet.get_image(382, 434, 42, 51).convert()
PLAYER_DEAD_2 = player_sheet.get_image(432, 445, 49, 40).convert()
PLAYER_DEAD_3 = player_sheet.get_image(492, 436, 38, 49).convert()
PLAYER_DEAD_4 = player_sheet.get_image(535, 459, 78, 24).convert()

##############################################################

sniper_sheet = SpriteSheet(os.path.join(imgFolder, 'enemies.png'))

SNIPER_LEFT_DOWN = sniper_sheet.get_image(303, 560, 72, 128).convert()
SNIPER_LEFT = sniper_sheet.get_image(220, 587, 83, 105).convert()
SNIPER_LEFT_UP = sniper_sheet.get_image(488, 695, 74, 110).convert()

##############################################################

soldier_sheet = sniper_sheet  # Both the animations are there in the same sheet

SOLDIER_0 = soldier_sheet.get_image(49, 9, 83, 90).convert()
SOLDIER_1 = soldier_sheet.get_image(135, 9, 78, 103).convert()
SOLDIER_2 = soldier_sheet.get_image(216, 9, 51, 96).convert()
SOLDIER_3 = soldier_sheet.get_image(272, 9, 65, 96).convert()
SOLDIER_4 = soldier_sheet.get_image(339, 9, 83, 96).convert()
SOLDIER_5 = soldier_sheet.get_image(427, 9, 85, 92).convert()
SOLDIER_6 = soldier_sheet.get_image(519, 9, 65, 101).convert()
SOLDIER_7 = soldier_sheet.get_image(587, 9, 54, 99).convert()
SOLDIER_8 = soldier_sheet.get_image(648, 9, 67, 96).convert()

##############################################################

TANK_0 = pygame.image.load(os.path.join(imgFolder, 'tank.png'))

##############################################################

POWERUP_SLOW = pygame.image.load(os.path.join(imgFolder, 'slow.png')).convert()
POWERUP_BLINK = pygame.image.load(os.path.join(imgFolder, 'force.png')).convert()
POWERUP_BULLET = pygame.image.load(os.path.join(imgFolder, 'bullet_slow.png')).convert()

##############################################################

explosion_sheet = SpriteSheet(os.path.join(imgFolder, 'explosion.png'))

EXPLOSION_0 = explosion_sheet.get_image(0, 0, 69, 67).convert()
EXPLOSION_1 = explosion_sheet.get_image(69, 0, 69, 67).convert()
EXPLOSION_2 = explosion_sheet.get_image(139, 0, 69, 67).convert()
EXPLOSION_3 = explosion_sheet.get_image(209, 0, 69, 67).convert()
EXPLOSION_4 = explosion_sheet.get_image(279, 0, 69, 67).convert()

##############################################################

shoot_sound = pygame.mixer.Sound(os.path.join(soundFolder,'Shoot.wav'))
powerup_sound = pygame.mixer.Sound(os.path.join(soundFolder,'Powerup.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join(soundFolder,'Explosion.wav'))
hit_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'Hit.wav'))
jump_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'Jump.wav'))
dash_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'Dash.wav'))
menu_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'menu.wav'))
#game_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'game.wav'))
pygame.mixer.music.set_volume(1)
