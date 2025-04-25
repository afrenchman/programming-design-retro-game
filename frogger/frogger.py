#! /usr/bin/env python
import pygame
import random as Random
from pygame.locals import *
from sys import exit
import os


pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

os.environ['SDL_VIDEO_CENTERED'] = '1' 
font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 20)
info_font = pygame.font.SysFont(font_name, 20)
menu_font = pygame.font.SysFont(font_name, 20)


screen = pygame.display.set_mode((1550,800), 0, 32)


if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick conectado: {joystick.get_name()}")
else:
    print("No se detectó ningún joystick.")

hat_x, hat_y = joystick.get_hat(0)

# Load the custom font
# Obtener el directorio del script actual (donde está frogger.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta relativa a la fuente desde el directorio del script
font_path = os.path.join(script_dir, 'Fonts', 'bit5x3.ttf')
# Cargar la fuente
game_font = pygame.font.Font(font_path, 70)
info_font = pygame.font.Font(font_path, 70)  # For the info font
menu_font = pygame.font.Font(font_path, 70)  # For the menu font


# --- Carregando imagens ---
# Obtener el directorio donde se encuentra el script actual (donde está frogger.py)
script_dir = os.path.dirname(os.path.abspath(__file__))

score_filename = os.path.join(script_dir, 'images', 'score2.png')
score_image = pygame.image.load(score_filename).convert_alpha()

score_filename3 = os.path.join(script_dir, 'images', 'score3.png')
score_image3 = pygame.image.load(score_filename3).convert_alpha()


# Construir las rutas relativas para las imágenes
background_filename = os.path.join(script_dir, 'images', 'bg2.png')
frog_filename = os.path.join(script_dir, 'images', 'sprite_sheets_up.png')
arrived_filename = os.path.join(script_dir, 'images', 'frog_arrived.png')
car1_filename = os.path.join(script_dir, 'images', 'car1.png')
car2_filename = os.path.join(script_dir, 'images', 'car2.png')
car3_filename = os.path.join(script_dir, 'images', 'car3.png')
car4_filename = os.path.join(script_dir, 'images', 'car4.png')
car5_filename = os.path.join(script_dir, 'images', 'car5.png')
plataform_filename = os.path.join(script_dir, 'images', 'tronco2.png')
turtle_filename = os.path.join(script_dir, 'images', 'Turtle_03.png')  # Nueva imagen de tortuga
home_filename = os.path.join(script_dir, 'images', 'Home.png')  # Imagen de los arbustos
fill_filename = os.path.join(script_dir, 'images', 'relleno.png')  # Ruta a la imagen de relleno

tortu_vida = os.path.join(script_dir, 'images', 'frog_arrived.png')  # Ruta a la imagen de relleno



frog_image = pygame.image.load(frog_filename).convert_alpha()
background = pygame.image.load(background_filename).convert()

background_width = background.get_width()  # Obtiene el ancho de la imagen
background_height = background.get_height()  # Obtiene la altura de la imagen

print(f"El tamaño de la imagen de fondo es: {background_width}x{background_height}")

sprite_sapo = pygame.image.load(frog_filename).convert_alpha()
sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
sprite_car1 = pygame.transform.scale(pygame.image.load(car1_filename).convert_alpha(), (38, 30))
sprite_car2 = pygame.transform.scale(pygame.image.load(car2_filename).convert_alpha(), (38, 30))
sprite_car3 = pygame.transform.scale(pygame.image.load(car3_filename).convert_alpha(), (38, 30))
sprite_car4 = pygame.transform.scale(pygame.image.load(car4_filename).convert_alpha(), (38, 30))
sprite_car5 = pygame.transform.scale(pygame.image.load(car5_filename).convert_alpha(), (55, 30))
sprite_plataform = pygame.transform.scale(pygame.image.load(plataform_filename).convert_alpha(), (100, 30))
sprite_turtle = pygame.transform.scale(pygame.image.load(turtle_filename).convert_alpha(), (30, 30))  # Escalar la tortuga si es necesario
# Escalar la imagen del arbusto a un tamaño mayor
sprite_home = pygame.transform.scale(pygame.image.load(home_filename).convert_alpha(), (70, 30))  # Cambiar dimensiones
# --- Escalar la imagen de relleno ---
sprite_fill = pygame.transform.scale(pygame.image.load(fill_filename).convert_alpha(), (50, 29))  # Ajustar el tamaño
sprite_tortuvida= pygame.image.load(tortu_vida).convert_alpha()
sprite_tortuvida = pygame.transform.flip(sprite_tortuvida, False, True)

# Construir las rutas relativas para los archivos de sonido
hit_sound_filename = os.path.join(script_dir, 'sounds', 'boom.wav')
agua_sound_filename = os.path.join(script_dir, 'sounds', 'agua.wav')
chegou_sound_filename = os.path.join(script_dir, 'sounds', 'success.wav')
trilha_sound_filename = os.path.join(script_dir, 'sounds', 'guimo.wav')

# Cargar los sonidos
hit_sound = pygame.mixer.Sound(hit_sound_filename)
agua_sound = pygame.mixer.Sound(agua_sound_filename)
chegou_sound = pygame.mixer.Sound(chegou_sound_filename)
trilha_sound = pygame.mixer.Sound(trilha_sound_filename)

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

screen_center_x = 1550 // 2
screen_center_y = 800 // 2

class Object():
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())


class Home(Object):
    def __init__(self, position, sprite_home):
        self.sprite = sprite_home
        self.position = position

    def draw(self):
        screen.blit(self.sprite, (self.position))

    def rect(self):
        return Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())

homes = []  # Lista para los arbustos


class Frog(Object):
    def __init__(self, position, sprite_sapo):
        self.sprite = sprite_sapo
        self.position = position
        self.lives = 3
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def updateSprite(self, key_pressed):
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_filename = os.path.join(script_dir, 'images', 'sprite_sheets_up.png')
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "down":
                frog_filename = os.path.join(script_dir, 'images', 'sprite_sheets_down.png')
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "left":
                frog_filename = os.path.join(script_dir, 'images', 'sprite_sheets_left.png')
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "right":
                frog_filename = os.path.join(script_dir, 'images', 'sprite_sheets_right.png')
                self.sprite = pygame.image.load(frog_filename).convert_alpha()

    def moveFrog(self, key_pressed, key_up):
        if self.animation_counter == 0:
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1]-13
            elif key_pressed == "down":
                if self.position[1] < 473:
                    self.position[1] = self.position[1]+13
            if key_pressed == "left":
                if self.position[0] > 565:
                    if self.animation_counter == 2:
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right": 
                if self.position[0] < 955: 
                    if self.animation_counter == 2:
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

    def animateFrog(self, key_pressed, key_up):
        if self.animation_counter != 0:
            if self.animation_tick <= 0:
                self.moveFrog(key_pressed, key_up)
                self.animation_tick = 1
            else:
                self.animation_tick = self.animation_tick - 1

    def setPos(self, position):
        self.position = position

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3:
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self, game):
        self.setPositionToInitialPosition()
        self.decLives()  # Disminuir vidas
        update_lives(self)  # Actualizar la cantidad de vidas
        game.resetTime()  # Resetear el tiempo
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def setPositionToInitialPosition(self):
        offset_x = (1550 - background.get_width()) // 2
        self.position = [207 + offset_x, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite, (self.position), (0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0], self.position[1], 30, 30)


def save_high_score(game):
    with open("high_score.txt", "w") as file:
        file.write(str(game.high_score))

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Si no se encuentra el archivo, el puntaje más alto será 0


    def moveFrog(self,key_pressed, key_up):
        #Tem que fazer o if das bordas da tela ainda
        #O movimento na horizontal ainda não ta certin
        if self.animation_counter == 0 :
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1]-13
            elif key_pressed == "down":
                if self.position[1] < 473:
                    self.position[1] = self.position[1]+13
            if key_pressed == "left":
                if self.position[0] > 2:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right":
                if self.position[0] < 401: 
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

    def animateFrog(self,key_pressed,key_up):
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.moveFrog(key_pressed,key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def setPos(self,position):
        self.position = position

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self, game):
        self.setPositionToInitialPosition()
        self.decLives()  # Disminuir vidas
        update_lives(self)  # Actualizar la cantidad de vidas
        game.resetTime()  # Resetear el tiempo
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def setPositionToInitialPosition(self):
        self.position = [1550 // 2 - 15, 800 - 75]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0],self.position[1],30,30)

class Enemy(Object):
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = sprite_enemy
        self.position = position
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor


class Plataform(Object):
    def __init__(self, position, sprite_plataform, way):
        self.sprite = sprite_plataform
        self.position = position
        self.way = way

    def move(self, speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed  # Troncos van a la derecha
        elif self.way == "left":
            self.position[0] = self.position[0] - speed  # Tortugas van a la izquierda


class Game():
    def __init__(self,speed,level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 30
        self.gameInit = 0
        self.high_score = load_high_score()  # Cargar el puntaje más alto al inicio

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self, points):
        self.points = self.points + points
        if self.points > self.high_score:  # Si el puntaje actual es mayor que el más alto
            self.high_score = self.points
            save_high_score(self)  # Guardar el nuevo puntaje más alto

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30



#Funções gerais
def drawList(list):
    for i in list:
        i.draw()


def moveList(list,speed):
    for i in list:
        i.move(speed)

def destroyEnemys(list):
    for i in list:
        if i.position[0] < 554:
            list.remove(i)
        elif i.position[0] > 950:
            list.remove(i)

def destroyPlataforms(list):
    for i in list:
        if i.position[0] < 480:
            list.remove(i)
        elif i.position[0] > 975:
            list.remove(i)

def createEnemys(list,enemys,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                position_init = [950, 436]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car1, "left", 1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [554, 397]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car2, "right", 2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [950, 357]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car3, "left", 2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                position_init = [554, 318]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car4, "right", 1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                position_init = [950, 280]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car5, "left", 1)
                enemys.append(enemy)


def createPlataform(list, plataforms, game, homes):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:  # Tres tortugas en fila (primera fila)
                list[0] = (30*game.speed)/game.level
                position_init1 = [554, 200]
                position_init2 = [554 + 30, 200]  # Tortuga 2 al lado de la primera
                position_init3 = [554 + 60, 200]  # Tortuga 3 al lado de la segunda
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")
                plataform3 = Plataform(position_init3, sprite_turtle, "right")
                plataforms.append(plataform1)
                plataforms.append(plataform2)
                plataforms.append(plataform3)

            elif i == 1:  # Tronco
                list[1] = (30*game.speed)/game.level
                position_init = [905, 161]
                plataform = Plataform(position_init, sprite_plataform, "left")  # Tortuga va a la izquierda
                plataforms.append(plataform)

            elif i == 2:  # Tronco
                list[2] = (40*game.speed)/game.level
                position_init = [905, 122]
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)

            elif i == 3:  # Dos tortugas en fila (cuarta fila)
                list[3] = (40*game.speed)/game.level
                position_init1 = [554, 83]  # Tortuga 1 en la cuarta fila
                position_init2 = [554 + 30, 83]  # Tortuga 2 al lado de la primera
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")  # Mover a la derecha
                plataforms.append(plataform1)
                plataforms.append(plataform2)

            elif i == 4:  # Troncos
                list[4] = (20 * game.speed) / game.level
                position_init_1 = [915, 44]  # Primer tronco
                position_init_2 = [980, 44]  # Segundo tronco, desplazado a la derecha
                plataform_1 = Plataform(position_init_1, sprite_plataform, "left")
                plataform_2 = Plataform(position_init_2, sprite_plataform, "left")
                plataforms.append(plataform_1)
                plataforms.append(plataform_2)


            # Agregar los arbustos en la parte inferior de la pantalla
            # Cambiar la posición de los arbustos a la parte superior de la pantalla
            position_init_fill = [550, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [564, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_home = [578, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos

            position_init_fill = [648, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)


                        # Agregar el segundo arbusto después del primero
            position_init_home2 = [662, 0]  # Mover un poco más a la derecha
            home_obj2 = Home(position_init_home2, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj2)  # Agregar el segundo arbusto


            position_init_fill = [732, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)


            position_init_home3 = [746, 0]  # Mover un poco más a la derecha
            home_obj3 = Home(position_init_home3, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj3)  # Agregar el segundo arbusto
 
            position_init_fill = [816, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_home4 = [830, 0]  # Mover un poco más a la derecha
            home_obj4 = Home(position_init_home4, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj4)  # Agregar el segundo arbusto

            position_init_fill = [900, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)            

            position_init_home5 = [914, 0]  # Mover un poco más a la derecha
            home_obj5 = Home(position_init_home5, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj5)  # Agregar el segundo arbusto            

            position_init_fill = [983, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)   





def frogOnTheStreet(frog,enemys,game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            hit_sound.play()
            frog.frogDead(game)

def frogInTheLake(frog,plataforms,game):
    #se o sapo esta sob alguma plataforma Seguro = 1
    seguro = 0
    wayPlataform = ""
    for i in plataforms:
        plataformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(plataformRect):
            seguro = 1
            wayPlataform = i.way

    if seguro == 0:
        agua_sound.play()
        frog.frogDead(game)

    elif seguro == 1:
        if wayPlataform == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif wayPlataform == "left":
            frog.position[0] = frog.position[0] - game.speed
#FALTA EDITAR ESTO 
def frogArrived(frog,chegaram,game):
    if frog.position[0] > 580 and frog.position[0] < 600:
        position_init = [599,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 664 and frog.position[0] < 684:
        position_init = [683,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 748 and frog.position[0] < 768:
        position_init = [767,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 832 and frog.position[0] < 850:
        position_init = [849,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 914 and frog.position[0] < 950:
        position_init = [932,7]
        createArrived(frog,chegaram,game,position_init)

    else:
        frog.position[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1


def whereIsTheFrog(frog):
    #Se o sapo ainda não passou da estrada
    if frog.position[1] > 240 :
        frogOnTheStreet(frog,enemys,game)

    #Se o sapo chegou no rio
    elif frog.position[1] < 240 and frog.position[1] > 40:
        frogInTheLake(frog,plataforms,game)

    #sapo chegou no objetivo
    elif frog.position[1] < 40 :
        frogArrived(frog,chegaram,game)


# Load the image for the time bar (assuming a width of 100)
time_bar_image = pygame.Surface((100, 10))  # Time bar of width 100 and height 10
time_bar_image.fill((0, 255, 0))  # Green color for the time bar

# --- Cambios en la función que dibuja las ranas ---
# --- Cambios en la función que dibuja las ranas --- 
def draw_lives(frog, x_position, y_position):
    """Dibuja las ranas en la pantalla según las vidas restantes."""
    for i in range(frog.lives):  # Solo dibujar las ranas que correspondan a las vidas restantes
        screen.blit(sprite_tortuvida, (x_position + i * 35, y_position))  # Dibuja las ranas con espacio entre ellas


def update_lives(frog):
    """Actualizar las vidas cuando se pierda una."""
    if frog.lives < 0:
        frog.lives = 0  # Evitar que las vidas sean negativas

def draw_time_bar(game):
    """Dibuja la barra de tiempo que se reduce de izquierda a derecha."""
    time_left = game.time  # El tiempo actual en segundos
    total_time = 30  # Total de tiempo disponible (30 segundos en este caso)
    
    # El ancho total de la barra es de 100 píxeles, así que calculamos el ancho que debe tener la barra verde
    bar_width = int((time_left / total_time) * 100)  # La barra verde se reducirá según el tiempo restante

    # Dibuja la barra negra (fondo) primero
    pygame.draw.rect(screen, (0, 0, 0), (700, 660, 100, 40))  # Barra negra de fondo
    #tiempo time
    # Luego dibuja la barra verde (tiempo restante)
    pygame.draw.rect(screen, (0, 255, 0), (700, 660, bar_width, 40))  # Barra verde que disminuye
    
    # Dibuja la palabra "TIME" a la derecha de la barra
    time_text = menu_font.render("TIME", True, (255, 255, 0))  # Color blanco para el texto
    screen.blit(time_text, (700, 600))  # Ajustamos la posición para que siempre esté a la derecha de la barra


def draw_score(game):
    # "HI-SCORE" en blanco y puntaje en rojo
    high_score_value_text = menu_font.render(f"{game.high_score:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(high_score_value_text, (1060, 280))  # Adjust the position for the "HI-SCORE" score



    one_up_value_text = menu_font.render(f"{game.points:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(one_up_value_text, (315, 270))  # Adjust the position for the "1-UP" score


def createArrived(frog,chegaram,game,position_init):
    sapo_chegou = Object(position_init,sprite_arrived)
    chegaram.append(sapo_chegou)
    chegou_sound.play()
    frog.setPositionToInitialPosition()
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1


def nextLevel(chegaram,enemys,plataforms,frog,game):
    if len(chegaram) == 5:
        chegaram[:] = []
        frog.setPositionToInitialPosition()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()


trilha_sound.play(-1)
text_info = menu_font.render(('Press any button to start!'),1,(0,0,0))
gameInit = 0

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == pygame.JOYBUTTONDOWN:  # Cualquier botón del joystick
            gameInit = 1  # Iniciar el juego    
        
        if event.type == pygame.JOYHATMOTION:
            hat_x, hat_y = event.value
            if hat_y == 1 or hat_y == -1 or hat_x == 1 or hat_x == -1:
                gameInit = 1

    # Centrar el fondo horizontalmente, mantenerlo arriba
    bg_rect = background.get_rect()
    bg_rect.topleft = ((1550 - background.get_width()) // 2, 0)
    screen.blit(background, bg_rect)
    # Dibujar la imagen de score en la posición (0, 0)
    screen.blit(score_image, (250, 0))
    screen.blit(score_image3, (995, -10))

    # Centrar el texto horizontalmente
    text_rect = text_info.get_rect(center=(1550 // 2, 310))
    pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 10))  # Añade algo de espacio extra con inflate

# Luego, dibuja el texto encima del cuadro
    screen.blit(text_info, text_rect)

    pygame.display.update()



while True:
    gameInit = 1
    game = Game(3, 1)
    key_up = 1
    offset_x = (1550 - background.get_width()) // 2
    frog_initial_position = [207 + offset_x, 475]
    frog = Frog(frog_initial_position, sprite_sapo)


    enemys = []
    plataforms = []
    chegaram = []
    ticks_enemys = [30, 0, 30, 0, 60]
    ticks_plataforms = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while frog.lives > 0:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            # Detectar si el D-pad del mando se mueve
            if event.type == pygame.JOYHATMOTION:
                # Obtener el estado del D-pad
                hat_x, hat_y = event.value

                # Detectar las direcciones del D-pad
                if hat_y == 1:  # Arriba
                    key_pressed = "up"
                    if frog.can_move == 1:
                        frog.moveFrog(key_pressed, 1)  # Mover la rana hacia arriba
                        frog.cannotMove()
                elif hat_y == -1:  # Abajo
                    key_pressed = "down"
                    if frog.can_move == 1:
                        frog.moveFrog(key_pressed, 1)  # Mover la rana hacia abajo
                        frog.cannotMove()
                elif hat_x == 1:  # Derecha
                    key_pressed = "right"
                    if frog.can_move == 1:
                        frog.moveFrog(key_pressed, 1)  # Mover la rana hacia la derecha
                        frog.cannotMove()
                elif hat_x == -1:  # Izquierda
                    key_pressed = "left"
                    if frog.can_move == 1:
                        frog.moveFrog(key_pressed, 1)  # Mover la rana hacia la izquierda
                        frog.cannotMove()

        # Aquí van el resto de las acciones y actualizaciones del juego


        if not ticks_time:
            ticks_time = 30
            game.decTime()
        else:
            ticks_time -= 1

        if game.time == 0:
            frog.frogDead(game)

        createEnemys(ticks_enemys, enemys, game)
        createPlataform(ticks_plataforms, plataforms, game, homes)  # Pasar la lista de arbustos

        moveList(enemys, game.speed)
        moveList(plataforms, game.speed)

        whereIsTheFrog(frog)

        nextLevel(chegaram, enemys, plataforms, frog, game)

        # Mostrar los puntos actuales en la parte inferior
        #text_info1 = info_font.render(('Points: {1}'.format(game.level, game.points)), 1, (255, 255, 255))
        
        # Redibujar la pantalla con fondo y puntajes
        offset_x = (1550 - 450) // 2  # 550
        screen.blit(background, (offset_x, 0))
        # Dibujar la imagen de score en la posición (0, 0)
        screen.blit(score_image, (250, 0))
        screen.blit(score_image3, (995, -10))

        # Dibuja las vidas restantes
        draw_lives(frog, offset_x + 10, 520)
        # Dibuja los enemigos, plataformas y arbustos
        drawList(enemys)
        drawList(plataforms)
        drawList(chegaram)
        drawList(homes)  # Dibuja los arbustos
        draw_time_bar(game)

        frog.animateFrog(key_pressed, key_up)
        frog.draw()

        destroyEnemys(enemys)
        destroyPlataforms(plataforms)

        # Dibuja la puntuación actual y la puntuación más alta en la parte superior
        
        screen.blit(score_image, (250, 0))
        screen.blit(score_image3, (995, -10))
        draw_score(game)
        pygame.display.update()
        time_passed = clock.tick(30)

    # Inicialización del joystick (esto debe estar antes de usarlo)
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # Verificar si el botón A (generalmente el 0) es presionado
        if joystick.get_button(0):  # El botón A por defecto
            gameInit = 0  # Reiniciar el juego

        # Dibujar la pantalla de "GAME OVER"
        screen.blit(background, (offset_x, 0))
        screen.blit(score_image, (250, 0))
        screen.blit(score_image3, (995, -10))


        text = game_font.render('GAME OVER', 1, (255, 0, 0))
        text_points = game_font.render(('Score: {0}'.format(game.points)), 1, (255, 0, 0))
        text_reiniciar = info_font.render('Press A to reset!', 1, (255, 0, 0))  # Texto actualizado
        text_rect = text.get_rect(center=(1550 // 2, 120))
        screen.blit(text, text_rect)

        points_rect = text_points.get_rect(center=(1550 // 2, 170))
        screen.blit(text_points, points_rect)

        reiniciar_rect = text_reiniciar.get_rect(center=(1550 // 2, 250))
        screen.blit(text_reiniciar, reiniciar_rect)


        pygame.display.update()


