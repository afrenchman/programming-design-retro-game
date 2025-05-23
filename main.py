import pygame
import sys
import subprocess
import os
import Donkey_Kong.game_mk
import frogger.frogger
import Tetris.tetris
import FinalContra.game


# Inicialización de Pygame
pygame.init()

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Configuración de la pantalla
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Retro Game Console')

# Cargar la imagen de fondo
background_image = pygame.image.load('./images_menu/background2.png')  # Cargar el fondo
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Ajustar tamaño

# Cargar las miniaturas de los juegos
game_images = [
    pygame.image.load('./images_menu/frogger.jpg'),  # Miniatura de Juego 1
    pygame.image.load('./images_menu/DonkeyKong.jpg'),  # Miniatura de Juego 2
    pygame.image.load('./images_menu/Tetris.jpg'),  # Miniatura de Juego 3
    pygame.image.load('./images_menu/Contra.jpg')   # Miniatura de Juego 4
]

# Ajustar tamaño de las imágenes de los juegos
game_images = [pygame.transform.scale(img, (200, 200)) for img in game_images]

# Fuente para el texto
font = pygame.font.SysFont('Arial', 50)
description_font = pygame.font.SysFont('Arial', 30)

# Índice de juego seleccionado
selected_index = 0

# Descripciones de los juegos
game_descriptions = [
    "Frogger 1998\nOne-Player\nClassic arcade action\nNavigate the frog across the road and river.",
    "Donkey Kong 1981\nOne-Player\nClassic arcade platformer\nHelp Mario rescue Pauline from Donkey Kong!",
    "Tetris 1984\nSingle-Player\nClassic puzzle game\nFit falling blocks to complete lines and clear the board!",
    "Contra 1987\nSingle-Player\n Side-scroller shooter game\nFight through the enemies in the jungle and beat the boss!"
    ]

# Variable para manejar el "debounce" de teclas
last_key_time = 0
key_delay = 300  # 300 ms de retraso entre presionar teclas

# Inicializar Joystick
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

# Verificar si hay joysticks conectados
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

# Función para dibujar el menú
def draw_menu():
    # Dibujar el fondo
    screen.blit(background_image, (0, 0))

    # Título
    title_text = font.render('SELECT GAME', True, RED)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 180))

    # Mostrar las miniaturas de los juegos
    for i, img in enumerate(game_images):
        x_position = screen_width // 2 - (len(game_images) * 220) // 2 + i * 220
        y_position = 300

        # Dibujar el cuadro alrededor del juego seleccionado
        if i == selected_index:
            pygame.draw.rect(screen, RED, (x_position - 10, y_position - 10, 220, 220), 5)

        screen.blit(img, (x_position, y_position))

    # Mostrar la descripción del juego seleccionado
    description_text = game_descriptions[selected_index]
    description_lines = description_text.split("\n")
    for i, line in enumerate(description_lines):
        text_surface = description_font.render(line, True, WHITE)
        screen.blit(text_surface, (screen_width // 2 - text_surface.get_width() // 2, 550 + i * 40))

    # Instrucciones
    instructions_text = font.render('Use D-Pad (Left/Right) to select, Press A to confirm', True, BLUE)
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, screen_height - 100))

    pygame.display.update()

# Función para manejar la entrada del usuario
def handle_input():
    global selected_index, last_key_time
    keys = pygame.key.get_pressed()

    # Comprobar si han pasado suficientes milisegundos entre las teclas
    current_time = pygame.time.get_ticks()
    if current_time - last_key_time > key_delay:
        # Manejar entrada del joystick (D-pad para izquierda/derecha)
        if joystick_count > 0:
            # D-pad izquierdo (mueve izquierda)
            if joystick.get_hat(0)[0] == -1:  # Flecha izquierda
                selected_index = (selected_index - 1) % len(game_images)
                last_key_time = current_time
            # D-pad derecho (mueve derecha)
            elif joystick.get_hat(0)[0] == 1:  # Flecha derecha
                selected_index = (selected_index + 1) % len(game_images)
                last_key_time = current_time

            # Botón A (seleccionar)
            if joystick.get_button(0):  # El botón A por defecto
                print(f"Game {selected_index + 1} selected")
                if selected_index == 0:
                    frogger.frogger.run_frogger()
                elif selected_index == 1:
                    Donkey_Kong.game_mk.run_mk()
                elif selected_index == 2:
                    Tetris.tetris.tetris_play()
                elif selected_index == 3:
                    FinalContra.game.run_fc()
                

# Ciclo principal
def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Dibujar el menú y manejar la entrada
        draw_menu()
        handle_input()

        clock.tick(60)  # Mantener la tasa de fotogramas a 60 FPS

# Iniciar el juego
if __name__ == '__main__':
    main()
