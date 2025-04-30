import os
import random
import sys
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
ss_press_play = pygame.image.load(os.path.join(imgFolder,'press_play.png')).convert()

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
game_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'game.mp3'))
over_sound = pygame.mixer.Sound(os.path.join(soundFolder, 'over.mp3'))
pygame.mixer.music.set_volume(1)

vec = pygame.math.Vector2

class Camera(object):
    def __init__(self, width, height):
        self.pos = vec(0,0)
    def update(self,sprite):
        if sprite.canMove:
            self.pos.x = -sprite.pos.x
        if self.pos.x >= LEFT_BOUND:
            self.pos.x = LEFT_BOUND
        elif self.pos.x <= RIGHT_BOUND:
            self.pos.x = RIGHT_BOUND
        #self.pos.y = min(-sprite.pos.y+HEIGHT/2,0)
        #print(self.pos.x)

camera = Camera(WIDTH,HEIGHT)

all_sprites = pygame.sprite.Group()

# Player States
RIGHT = 0
LEFT = 1
RIGHT_DOWN = 2
RIGHT_UP = 3
LEFT_UP = 4
LEFT_DOWN = 5

#####################################################################################################
# PLAYER SPRITE HANDLING                                                                                          #
#####################################################################################################

class Player(pygame.sprite.Sprite):
    def __init__(self, game):

        pygame.sprite.Sprite.__init__(self)
        self.game = game

        self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (PLAYER_POSX, 0)
        self.health = PLAYER_HEALTH

        # Movement
        self.joystick = self.game.joystick
        self.state = RIGHT
        self.up = False
        self.down = False
        self.pos = vec(30, 30)
        self.vel = vec(0, 0)
        self.acc = vec(0, GRAVITY)
        self.canMove = True
        self.jumping = True
        self.facing = 1

        # Jumping
        self.canJump = False
        self.collisions = True

        # Blinking
        self.blinkTime = BLINK_TIME
        self.canBlink = 1
        self.blinking = False
        self.blinkRetract = BLINK_RETRACT

        self.dead = False
        # Animation
        # Frames hold each frame
        # index determines the current frame to be played
        self.animCounter = ANIM_SPEED

        self.jumpFrames = [PLAYER_JUMP_0, PLAYER_JUMP_1, PLAYER_JUMP_2, PLAYER_JUMP_3]
        self.jumpIndex = 0

        self.rightFrames = [PLAYER_RIGHT_0, PLAYER_RIGHT_1, PLAYER_RIGHT_2, PLAYER_RIGHT_3, PLAYER_RIGHT_4,
                            PLAYER_RIGHT_5]
        self.rightIndex = 0

        self.rightUpFrames = [PLAYER_RIGHT_UP_0, PLAYER_RIGHT_UP_1, PLAYER_RIGHT_UP_2]
        self.rightUpIndex = 0

        self.rightDownFrames = [PLAYER_RIGHT_DOWN_0, PLAYER_RIGHT_DOWN_1, PLAYER_RIGHT_DOWN_2]
        self.rightDownIndex = 0

        self.deadFrames = [PLAYER_DEAD_0, PLAYER_DEAD_1, PLAYER_DEAD_2, PLAYER_DEAD_3, PLAYER_DEAD_4]
        self.deadIndex = 0

    def update(self):
        self.calcState()
        if self.dead:
            self.kill()
            return
        if self.jumping:
            self.jumpIndex = self.animate(self.jumpFrames, self.jumpIndex, int(PLAYER_HEIGHT / 2), PLAYER_WIDTH)

        else:
            self.setImageByState()
            if self.isMoving():
                # Set the animation depending on the state
                if self.state == RIGHT:
                    self.rightIndex = self.animate(self.rightFrames, self.rightIndex, PLAYER_WIDTH, PLAYER_HEIGHT)
                elif self.state == RIGHT_DOWN:
                    self.rightDownIndex = self.animate(self.rightDownFrames, self.rightDownIndex, PLAYER_WIDTH,
                                                       PLAYER_HEIGHT)
                elif self.state == RIGHT_UP:
                    self.rightUpIndex = self.animate(self.rightUpFrames, self.rightUpIndex, PLAYER_WIDTH, PLAYER_HEIGHT)
                elif self.state == LEFT:
                    self.rightIndex = self.animate(self.rightFrames, self.rightIndex, PLAYER_WIDTH, PLAYER_HEIGHT, True)
                elif self.state == LEFT_DOWN:
                    self.rightDownIndex = self.animate(self.rightDownFrames, self.rightDownIndex, PLAYER_WIDTH,
                                                       PLAYER_HEIGHT, True)
                elif self.state == LEFT_UP:
                    self.rightUpIndex = self.animate(self.rightUpFrames, self.rightUpIndex, PLAYER_WIDTH, PLAYER_HEIGHT,
                                                     True)
            else:
                # Else a stationary image
                if self.state == RIGHT:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == RIGHT_DOWN:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_DOWN_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == RIGHT_UP:
                    self.image = pygame.transform.scale(PLAYER_RIGHT_UP_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
                elif self.state == LEFT:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
                elif self.state == LEFT_DOWN:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_DOWN_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)
                elif self.state == LEFT_UP:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(PLAYER_RIGHT_UP_0, (PLAYER_WIDTH, PLAYER_HEIGHT)), True, False)

        if self.blinking:
            self.acc = vec(0, 0)
            self.vel.y = 0
            self.vel.x = self.facing * BLINK_SPEED
            self.blinkTime -= 1
            self.blinkRetract -= 1
            if self.blinkTime == 0:
                self.blinking = False
                self.blinkTime = BLINK_TIME
                self.blinkRetract = BLINK_RETRACT
        else:
            self.acc = vec(0, GRAVITY)
            if self.blinkRetract == 0:
                pass
            else:
                self.blinkRetract -= 1

        if self.joystick:
            # D-Pad (Hat switch) movement
            hat_x, hat_y = self.joystick.get_hat(0)
            if hat_x < 0:  # Move left
                self.acc.x = -PLAYER_ACC
                self.facing = -1
            elif hat_x > 0:  # Move right
                self.acc.x = PLAYER_ACC
                self.facing = 1
            else:
                self.acc.x = 0

            # Right stick aiming for continuous movement or aiming
            right_x = self.joystick.get_axis(2)  # Right stick X axis
            right_y = self.joystick.get_axis(3)  # Right stick Y axis

            if abs(right_x) > 0.1 or abs(right_y) > 0.1:
                # Aim or shoot in the direction of the right analog stick
                aim_x = self.pos.x + (right_x * 100)
                aim_y = self.pos.y + (right_y * 100)
                # Shooting or other action can be implemented here

        # Apply physics and movement
        if not self.pos.x < -LEFT_BOUND and not self.pos.x > -RIGHT_BOUND:
            self.acc.x += self.vel.x * PLAYER_FRC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
        else:
            if self.pos.x <= -LEFT_BOUND:
                self.pos.x += 1
            else:
                self.pos.x -= 1

        # Update rect and image
        self.rect.bottom = self.pos.y
        self.image.set_colorkey(YELLOW)

    #####################################################################################################

    def isMoving(self):
        if int(self.vel.x):
            return True
        return False

    #####################################################################################################

    def jump(self):
        if self.canMove and self.canJump:
            self.vel.y = -JUMP_HEIGHT
            self.jumping = True
            self.canJump = False

    #####################################################################################################

    def move_left(self):
        self.acc.x = -PLAYER_ACC

    def move_right(self):
        self.acc.x = PLAYER_ACC

    def stop_moving(self):
        self.acc.x = 0

    #####################################################################################################

    def blink(self):
        if self.canMove and self.blinkRetract == 0:
            self.blinkRetract = BLINK_RETRACT
            dash_sound.play()
            self.blinking = True

    #####################################################################################################

    def stopJumping(self):
        self.jumpIndex = 0
        self.jumping = False

    #####################################################################################################

    def animate(self, frames, index, width, height, flip=False):
        self.animCounter -= 1
        if self.animCounter == 0:
            index += 1
            # print(index)
            index %= len(frames)
            if not flip:
                self.image = pygame.transform.scale(frames[index], (width, height))
            else:
                self.image = pygame.transform.flip(pygame.transform.scale(frames[index], (width, height)), True, False)
            self.animCounter = ANIM_SPEED
        rx = self.rect.left
        ry = self.rect.top
        self.rect = self.image.get_rect()
        self.rect.left = rx
        self.rect.top = ry
        return index

    #####################################################################################################

    def drop(self):
        if self.canMove:
            self.collisions = False

    #####################################################################################################

    def shoot(self, mousePos):
        self.calcState()
        if self.state == RIGHT:
            speedx, speedy = 1, 0
            pass
        elif self.state == LEFT:
            speedx, speedy = -1, 0
            pass
        elif self.state == RIGHT_UP:
            speedx, speedy = 1, 1
            pass
        elif self.state == RIGHT_DOWN:
            speedx, speedy = 1, -1
            pass
        elif self.state == LEFT_UP:
            speedx, speedy = -1, 1
            pass
        elif self.state == LEFT_DOWN:
            speedx, speedy = -1, -1
            pass
        shoot_sound.play()
        b = Bullet(PLAYER_POSX, self.pos.y, speedx, speedy)
        return b

    #####################################################################################################

    def calcState(self):
        # Get the right analog stick position
        right_x = self.joystick.get_axis(2)  # Right stick X (left-right)
        right_y = self.joystick.get_axis(3)  # Right stick Y (up-down)

        # Threshold for determining if the stick is in a "full" position
        threshold = 0.9

        # Determine the state based on the analog stick direction
        if right_y < -threshold:  # Stick is facing all the way up
            self.up = True
            self.down = False
        elif right_y > threshold:  # Stick is facing all the way down
            self.up = False
            self.down = True
        else:
            self.up = False
            self.down = False

        if abs(right_x) > threshold:  # Stick is facing all the way left or right
            self.state = "LEFT" if right_x < 0 else "RIGHT"
        elif abs(right_x) < 0.2 and abs(right_y) < 0.2:  # Stick is in a neutral position (near center)
            self.state = "NEUTRAL"
        else:
            self.state = "IDLE"  # A fallback state, can be used for fine adjustments

        if self.facing == 1:
            if self.up:
                self.state = RIGHT_UP
            elif self.down:
                self.state = RIGHT_DOWN
            else:
                self.state = RIGHT
        else:
            if self.up:
                self.state = LEFT_UP
            elif self.down:
                self.state = LEFT_DOWN
            else:
                self.state = LEFT

    #####################################################################################################

    def setImageByState(self):
        if self.state == RIGHT and not self.isMoving():
            self.image = pygame.transform.scale(PLAYER_RIGHT_0, (PLAYER_WIDTH, PLAYER_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect.left = PLAYER_POSX

    #####################################################################################################

    def die(self):
        print("DEAD")
        self.dead = True
        self.health = PLAYER_HEALTH

#####################################################################################################
# ENEMY SPRITE HANDLING                                                                             #
#####################################################################################################

class Sniper(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.up = False
        self.down = False
        self.speedy = 0
        self.defaultx = x
        self.defaulty = y
        self.counter = 60
        self.state = LEFT

    #####################################################################################################

    def update(self):
        # Update sprite image based on state
        if self.state == LEFT:
            self.image = pygame.transform.scale(SNIPER_LEFT, (PLAYER_WIDTH, PLAYER_HEIGHT))
        elif self.state == LEFT_UP:
            self.image = pygame.transform.scale(SNIPER_LEFT_UP, (PLAYER_WIDTH, PLAYER_HEIGHT))
        else:
            self.image = pygame.transform.scale(SNIPER_LEFT_DOWN, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.set_colorkey(YELLOW)
        self.rect.x = self.defaultx + camera.pos.x
        self.rect.y = self.defaulty + camera.pos.y
        pass

    #####################################################################################################

    def shoot_towards(self, player):
        # print(str(player.rect.bottom)+","+str(self.rect.bottom))
        if player.rect.top < self.rect.top:
            self.down = True
            self.up = False
            self.state = LEFT_DOWN
        elif player.rect.center[1] > self.rect.bottom:
            self.up = True
            self.down = False
            self.state = LEFT_UP
        else:
            self.up, self.down = False, False
            self.state = LEFT
        if self.rect.x < PLAYER_POSX + SNIPER_RANGE and self.rect.x > PLAYER_POSX:
            if self.counter == 0:
                self.counter = 60
                return self.shoot(self.up, self.down)
            else:
                self.counter -= 1
                return None

    def shoot(self, up, down):
        sx = -1
        if up:
            sy = 1
        elif down:
            sy = -1
        else:
            sy = 0
        b = Bullet(self.rect.left, self.rect.bottom, sx, sy)
        return b

    #####################################################################################################

class Soldier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(SOLDIER_0, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH + x
        self.rect.bottom = -y
        self.pos = vec(WIDTH + x, -y)
        self.target_y = y
        self.vel = vec(-SOLDIER_SPEEDX, SOLDIER_SPEEDY)
        self.acc = vec(0, GRAVITY)
        # Animation
        self.soldier_frames = [SOLDIER_0, SOLDIER_1, SOLDIER_2, SOLDIER_3, SOLDIER_4, SOLDIER_5, SOLDIER_6, SOLDIER_7,
                               SOLDIER_8]
        self.animIndex = 0
        self.animCounter = ANIM_SPEED

    #####################################################################################################

    def animate(self):
        self.animCounter -= 1
        if self.animCounter == 0:
            self.animIndex += 1
            self.animIndex %= len(self.soldier_frames)
            self.image = pygame.transform.scale(self.soldier_frames[self.animIndex], (PLAYER_WIDTH, PLAYER_HEIGHT))
            self.animCounter = ANIM_SPEED
        self.image.set_colorkey(YELLOW)

    #####################################################################################################

    def update(self):
        if self.rect.right < 0:
            self.kill()
        self.animate()
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.x = self.pos.x + camera.pos.x
        self.rect.bottom = self.pos.y + camera.pos.y

    #####################################################################################################

    def shoot_towards(self, player):
        # Shoot towards the player.
        pass

    #####################################################################################################

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = TANK_0
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)
        self.counter = 60

    #####################################################################################################

    def update(self):
        self.rect.x = self.pos.x + camera.pos.x
        self.counter -= 1
        pass

    #####################################################################################################

    def shoot(self):
        if self.rect.x > PLAYER_POSX:
            if self.counter == 0 or self.counter == 5:
                if self.counter == 0:
                    self.counter = 60
                return Bullet(self.rect.x, self.rect.bottom, -1, 0)
        return None

#####################################################################################################
# BULLET SPRITE HANDLING                                                                            #
#####################################################################################################

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speedx, speedy):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.image.set_colorkey(WHITE)
        self.rect.left = x + 40
        self.rect.top = y - 100
        self.speedx = speedx
        self.speedy = speedy

    #####################################################################################################

    def update(self):
        self.rect.left += self.speedx * BULLET_SPEED
        self.rect.top += self.speedy * BULLET_SPEED
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

#####################################################################################################
# PLATFORM SPRITE HANDLING                                                                          #
#####################################################################################################

class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.defaultx = x
        self.defaulty = y

    #####################################################################################################

    def update(self):
        self.rect.x = self.defaultx + camera.pos.x
        # print("Ground : "+str(self.rect.x))
        self.rect.y = self.defaulty + camera.pos.y


#####################################################################################################
# BG SPRITE HANDLING                                                                                #
#####################################################################################################

class Background(pygame.sprite.Sprite):
    def __init__(self, bg):
        pygame.sprite.Sprite.__init__(self)
        self.image = bg
        self.rect = self.image.get_rect()
        self.rect.left = camera.pos.x
        self.rect.y = camera.pos.y

    def update(self):
        self.rect.x = camera.pos.x
        self.rect.y = camera.pos.y

#####################################################################################################
# HUD                                                                                               #
#####################################################################################################

class HUD(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        pygame.font.init()
        self.surface = pygame.Surface((WIDTH, 40))
        self.surface.fill(WHITE)
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        self.font = pygame.font.SysFont("monospace", 20)
    def update(self):
        pass

    def update_HUD(self, game):
        self.surface = pygame.Surface((WIDTH, 30))
        self.surface.fill(LIGHT_YELLOW)
        self.drawHealth(game.health)
        self.drawBlink(game.blinkRetract)
        self.drawPowerup()
        pass

    def drawHealth(self, health):
        if health > PLAYER_HEALTH - 5:
            text = self.font.render("Health: " + str(health), 1, DARK_GREEN)
        elif health > 10:
            text = self.font.render("Health: " + str(health), 1, DARK_YELLOW)
        else:
            text = self.font.render("Health: " + str(health), 1, RED)
        textPos = text.get_rect()
        textPos.centerx = 130
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawBlink(self, retract):
        retractPerc = str(100 - int(retract / BLINK_RETRACT * 100))
        if retractPerc == '100':
            retractPerc = "READY"
            text = self.font.render("Dash: " + retractPerc, 1, DARK_GREEN)
        else:
            text = self.font.render("Dash: " + retractPerc, 1, RED)
        textPos = text.get_rect()
        textPos.centerx = 410
        self.surface.blit(text, textPos)
        self.image = self.surface

    def drawPowerup(self):
        pass

#####################################################################################################
# POWERUP                                                                                           #
#####################################################################################################

class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, ptype):
        pygame.sprite.Sprite.__init__(self)
        if ptype == 1:
            self.image = POWERUP_BULLET
        elif ptype == 0:
            self.image = POWERUP_BLINK
        else:
            self.image = POWERUP_SLOW
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        if x > 6164:
            x = 6160
        self.rect.x = x
        self.defaultx = x
        self.rect.y = -5

        self.ptype = ptype

    def update(self):
        if not self.rect.y >= 1000:
            self.rect.y += POWERUP_SPEED

        self.rect.x = camera.pos.x + self.defaultx
        if self.rect.x < 0:
            self.kill()
        if self.rect.bottom >= HEIGHT-50:
            self.kill()

    def powerup(self):
        # perform the action of the powerup
        return self.ptype

#####################################################################################################
# DEATH                                                                                             #
#####################################################################################################

class Death(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = EXPLOSION_0
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.defaultx = x
        self.rect.top = y - 50
        self.time = 0
        self.image.set_colorkey(WHITE)
        self.explosionFrames = [EXPLOSION_0, EXPLOSION_1, EXPLOSION_2, EXPLOSION_3, EXPLOSION_4]
        explosion_sound.play()

    def update(self):
        # self.rect.left = self.defaultx + camera.pos.x
        self.time += 1
        if self.time == 5:
            self.kill()
            return
        self.image = self.explosionFrames[self.time]
        self.image.set_colorkey(WHITE)

        pass

def run_fc():
	class Game:
		def __init__(self):
			# Initialize
			size = width, height = 600, 480
			if "-f" in sys.argv[1:]:
				self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
			else:
				self.screen = screen
			pygame.display.set_caption(TITLE)
			self.clock = pygame.time.Clock()
			self.joystick = None
			self.init_joystick()
			self.running = True
			self.soldierTimer = SOLDIER_SPAWN_TIMER
			self.joystick = None
			pygame.joystick.init()
			if pygame.joystick.get_count() > 0:
				self.joystick = pygame.joystick.Joystick(0)
				self.joystick.init()
				print(f"Joystick connected: {self.joystick.get_name()}")
			else:
				print("No joystick detected - using keyboard controls")
			self.reinit()

		#####################################################################################################

		def reinit(self):
			self.all_sprites = pygame.sprite.Group()
			self.grounds = pygame.sprite.Group()
			self.player_sprite = pygame.sprite.Group()
			self.bg_sprite = pygame.sprite.Group()
			self.bullets = pygame.sprite.Group()
			self.snipers = pygame.sprite.Group()
			self.soldiers = pygame.sprite.Group()
			self.enemy_bullets = pygame.sprite.Group()
			self.tanks = pygame.sprite.Group()
			self.powerups = pygame.sprite.Group()
			self.bosses = pygame.sprite.Group()
			self.death_anims = pygame.sprite.Group()
			self.health = PLAYER_HEALTH
			self.soldierTimer = SOLDIER_SPAWN_TIMER
			self.powerupTimer = POWERUP_TIME
			self.blinkRetract = BLINK_RETRACT
			self.time = 0

		#####################################################################################################

		def init_joystick(self):
			pygame.joystick.init()
			if pygame.joystick.get_count() > 0:
				self.joystick = pygame.joystick.Joystick(0)
				self.joystick.init()
				print(f"Joystick detected: {self.joystick.get_name()}")

		#####################################################################################################

		def new(self):
			self.reinit()
			self.run()

		def run(self):
			self.playing = True
			while self.playing:
				self.clock.tick(FPS)
				self.events()
				self.update()
				self.draw()

		#####################################################################################################

		def deathAnim(self,sprite):
			death = Death(sprite.rect.left,sprite.rect.top)
			self.death_anims.add(death)
			self.all_sprites.add(death)

		#####################################################################################################

		def update(self):
			self.time += 1
			if not self.bosses:
				self.playing = False
			self.soldierTimer -= 1
			self.powerupTimer -= 1
			self.soldierTimer %= SOLDIER_SPAWN_TIMER
			if self.soldierTimer == 0:
				self.soldierTimer = SOLDIER_SPAWN_TIMER
				soldier = Soldier(random.randint(int(p.pos.x+600),int(p.pos.x+800)),random.randint(int(p.pos.y),int(p.pos.y+300)))
				self.soldiers.add(soldier)
				self.all_sprites.add(soldier)

			if self.powerupTimer == 0:
				self.powerupTimer = POWERUP_TIME
				po = Powerup(random.randint(int(p.pos.x+300),int(p.pos.x+600)),random.randint(0,3))
				self.powerups.add(po)
				self.all_sprites.add(po)
			self.health = p.health
			self.blinkRetract = p.blinkRetract
			self.all_sprites.update()
			h.update_HUD(self)
			camera.update(p)
			# Check if player fell off screen
			if p.rect.top > HEIGHT or p.rect.x < 0:
				p.die()
				self.deathAnim(p)
				self.playing = False
			# Check if any enemy dies
			h1 = pygame.sprite.groupcollide(gamer.bullets,gamer.snipers,True,True)
			if h1:
				for k in h1:
					self.deathAnim(k)
			h1 = pygame.sprite.groupcollide(gamer.bullets,gamer.soldiers,True,True)
			if h1:
				for k in h1:
					self.deathAnim(k)
			h1 = pygame.sprite.groupcollide(gamer.bullets,gamer.tanks,True,True)
			if h1:
				for k in h1:
					self.deathAnim(k)

			# Player collision with bullets!
			hits = pygame.sprite.spritecollide(p,gamer.enemy_bullets,True)
			if hits:
				p.health -= 1
				hit_sound.play()
				if p.health == 0:
					p.die()
					self.deathAnim(p)
					self.playing = False

			# or enemy
			h1 = pygame.sprite.spritecollide(p,gamer.snipers,False)
			if h1:
				p.die()
				self.deathAnim(p)
				self.playing = False
			h1 =  pygame.sprite.spritecollide(p,gamer.soldiers,False)
			if h1:
				p.die()
				self.deathAnim(p)
				self.playing = False
			h1 = pygame.sprite.spritecollide(p,gamer.tanks,False)
			if h1:
				p.die()
				self.deathAnim(p)
				self.playing = False


			# Sniper events ###################################################################################################
			for e in self.snipers:
				b = e.shoot_towards(p)
				if b:
					self.enemy_bullets.add(b)
					self.all_sprites.add(b)

			# Tank Events #####################################################################################################
			for t in self.tanks:
				b = t.shoot()
				if b:
					self.enemy_bullets.add(b)
					self.all_sprites.add(b)

			# Do not jump up a platform if the full body is not yet above the platform
			hits = pygame.sprite.spritecollide(p,gamer.grounds,False)
			if hits and p.collisions and p.vel.y <= 0:
				p.collisions = False

			# Enable collisions when body out of ground
			if not hits and not p.collisions:
				p.collisions = True

			# Jump on platform only while falling
			if p.vel.y > 0 and p.collisions:
				if hits:
					p.pos.y = hits[0].defaulty
					p.stopJumping()
					p.vel.y = 0
					p.canJump = True
			for e in self.soldiers:
				hits = pygame.sprite.spritecollide(e,gamer.grounds,False)
				if hits :
					e.pos.y = hits[0].defaulty
					e.vel.y = 0

			# Continuous joystick inputs
			if self.joystick and not p.dead:
				axis_0 = self.joystick.get_axis(0)
				hat_x, _ = self.joystick.get_hat(0)

				# Prioritize analog stick if moved
				if abs(axis_0) > 0.5:
					if axis_0 < 0:
						p.move_left()
					else:
						p.move_right()
				# D-Pad support
				elif hat_x != 0:
					if hat_x < 0:
						p.move_left()
					else:
						p.move_right()
				else:
					p.stop_moving()

				# Right stick aiming
				if abs(self.joystick.get_axis(2)) > 0.1 or abs(self.joystick.get_axis(3)) > 0.1:
					aim_x = p.pos.x + (self.joystick.get_axis(2) * 100)
					aim_y = p.pos.y + (self.joystick.get_axis(3) * 100)

			# Powerup events
			hits = pygame.sprite.spritecollide(p,gamer.powerups,False)
			if hits:
				powerup = hits[0]
				action = powerup.powerup()
				powerup_sound.play()
				if action == 0:
					p.blinkRetract = 0
					self. blinkRetract = 0
				elif action == 1:
					p.health += 1
					self.health += 1
				else:
					p.drop()
				powerup.kill()

		#####################################################################################################

		def events(self):
			# Check for joystick connection
			joystick_connected = pygame.joystick.get_count() > 0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					if self.playing:
						self.playing = False
					self.running = False
					pygame.quit()
					quit()

				# Always process joystick events if connected
				if joystick_connected and event.type == pygame.JOYBUTTONDOWN and not p.dead:
					if event.button == 0:  # A button | JUMP
						p.jump()
						jump_sound.play()
					if event.button == 1:  # B button | SHOOT
						x_axis = self.joystick.get_axis(2)
						y_axis = self.joystick.get_axis(3)
						if abs(x_axis) > 0.1 or abs(y_axis) > 0.1:
							aim_x = p.pos.x + x_axis * 100
							aim_y = p.pos.y + y_axis * 100
							b = p.shoot((aim_x,aim_y))
							self.all_sprites.add(b)
							self.bullets.add(b)
					if event.button == 2:  # X button | QUIT
						self.playing = False
						return "restart"
					if event.button == 3:  # Y button | DROP
						p.drop()

		#####################################################################################################

		def draw(self):
			self.screen.fill(BLACK)
			self.grounds.draw(self.screen)
			self.bg_sprite.draw(self.screen)
			self.player_sprite.draw(self.screen)
			self.snipers.draw(self.screen)
			self.soldiers.draw(self.screen)
			self.enemy_bullets.draw(self.screen)
			self.bullets.draw(self.screen)
			self.tanks.draw(self.screen)
			self.bosses.draw(self.screen)
			self.powerups.draw(self.screen)
			pygame.draw.rect(self.screen,SEA_BLUE,(0,1000,15000,100))
			self.death_anims.draw(self.screen)
			pygame.display.update()

		def draw_text(self, text, size, x, y):
			font_name = pygame.font.match_font('Times')
			font = pygame.font.Font(font_name, size)
			text_surface = font.render(text, True, RED)
			text_rect = text_surface.get_rect()
			text_rect.center = (x, y)
			self.screen.blit(text_surface, text_rect)
			pygame.display.update()

		#####################################################################################################

		def show_start_screen(self):
			# Initial position - start off screen to the right
			menu_x = WIDTH
			target_x = (WIDTH - ss_background.get_width()) // 2
			menu_y = (HEIGHT - ss_background.get_height()) // 2

			# Animation parameters
			animation_speed = 8
			animation_complete = False

			# Slide-in animation
			while not animation_complete:
				self.screen.fill(BLACK)

				# Update menu position
				if menu_x > target_x:
					menu_x -= animation_speed
					if menu_x <= target_x:
						menu_x = target_x
						animation_complete = True
						menu_sound.play()

				# Draw menu
				self.screen.blit(ss_background, (menu_x, menu_y))
				pygame.display.flip()
				self.clock.tick(FPS)

				# Exit handling
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						quit()

			# Blinking image setup
			waiting_for_start = True
			blink_visible = True
			last_blink_time = pygame.time.get_ticks()
			blink_interval = 200  # milliseconds

			while waiting_for_start:
				self.screen.blit(ss_background, (target_x, menu_y))

				# Blinking logic
				current_time = pygame.time.get_ticks()
				if current_time - last_blink_time > blink_interval:
					blink_visible = not blink_visible
					last_blink_time = current_time

				if blink_visible:
					self.screen.blit(ss_press_play, (350, 700))

				pygame.display.update()

				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						waiting_for_start = False
						pygame.quit()
						quit()
					if event.type == pygame.JOYBUTTONDOWN:
						if event.button == 0:
							waiting_for_start = False
							menu_sound.stop()
							game_sound.play()

		#####################################################################################################

		def show_game_over_screen(self):
			game_sound.stop()
			over_sound.play()
			waiting_for_die = True
			joystick_connected = pygame.joystick.get_count() > 0

			while waiting_for_die:
				self.screen.blit(game_over,game_over.get_rect())
				pygame.display.update()
				for event in pygame.event.get():
					if joystick_connected and event.type == pygame.JOYBUTTONDOWN:
						if event.button == 1:
							over_sound.stop()
							game_sound.play()
							return "restart"
						if event.button == 0:
							self.running = False
							pygame.quit()
							quit()

			if not self.bosses:
				text_to_display = "STAGE CLEAR ("+str(int(self.time/FPS))+" s)"
			pygame.draw.rect(self.screen,WHITE,(WIDTH/2, HEIGHT/2 - 35, 200,50))
			self.draw_text(text_to_display, 21, WIDTH/2 + 100, HEIGHT/2 - 20)
			self.draw_text("R to restart, Q to quit", 21,WIDTH/2 + 100, HEIGHT/ 2)

	#####################################################################################################
	# GAME NETWORK																						#
	#####################################################################################################

	# init game
	gamer = Game()
	gamer.show_start_screen()
	gamer.running = True

	while gamer.running:
		# init player
		p = Player(gamer)
		gamer.reinit()
		gamer.player_sprite.add(p)
		gamer.all_sprites.add(p)


		# init level
		for ground in LEVEL_1:
			gs = Ground(*ground)
			gamer.all_sprites.add(gs)
			gamer.grounds.add(gs)

		# init level background based on level
		bg = Background(l1_bg)
		gamer.bg_sprite.add(bg)
		gamer.all_sprites.add(bg)

		# init snipers
		for s in LEVEL_1_SNIPERS:
			sn = Sniper(*s)
			gamer.snipers.add(sn)
			gamer.all_sprites.add(sn)

		# init soldiers
		for sol in LEVEL_1_SOLDIERS:
			s = Soldier(*sol)
			gamer.soldiers.add(s)
			gamer.all_sprites.add(s)

		# init tanks
		for t in LEVEL_1_TANKS:
			tank = Tank(*t)
			gamer.tanks.add(tank)
			gamer.all_sprites.add(tank)

		for po in LEVEL_1_PUPS:
			pup = Powerup(*po)
			gamer.powerups.add(pup)
			gamer.all_sprites.add(pup)

		# Boss
		for boss in LEVEL_1_BOSSES:
			b = Tank(*boss)
			gamer.bosses.add(b)
			gamer.tanks.add(b)
			gamer.all_sprites.add(b)

		# HUD
		h = HUD()
		gamer.player_sprite.add(h)
		gamer.all_sprites.add(h)
		# Start a new game
		gamer.run()
		result = gamer.show_game_over_screen()
		if result == "restart":
			continue
		else:
			break

if __name__ == "__main__":
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pygame.init()
	run_fc()
	pygame.quit()
