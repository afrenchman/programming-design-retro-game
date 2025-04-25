import pygame,sys
from game import Game
from colors import Colors
from button import Button
import os

pygame.init()


pygame.joystick.init()
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick connected: {joystick.get_name()}")
else:
    joystick = None
    print("No joystick.")


screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Tetris")

current_dir = os.path.dirname(os.path.abspath(__file__))

BG = pygame.image.load(current_dir + "/assets/background.jpg")

def get_font(size): 
    return pygame.font.Font(current_dir + "/assets/font.ttf", size)

def easy():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Easy Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,350)

    selected_option = 0  # 0 = Start Over, 1 = Quit

    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Movimiento con teclado
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_SPACE:
                    game.rotate()

            # Movimiento con D-Pad del control
            if event.type == pygame.JOYHATMOTION and not game.game_over:
                hat_x, hat_y = event.value
                if hat_x == -1:
                    game.move_left()
                elif hat_x == 1:
                    game.move_right()
                if hat_y == -1:
                    game.move_down()
                    game.update_score(0, 1)


            # Botón A para rotar
            if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                if event.button == 0:
                    game.rotate()

            if event.type == game_update and game.game_over == False:
                game.move_down()



# Movimiento en Game Over
            if game.game_over:
                if event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = event.value
                    if hat_y == -1 or hat_y == 1:
                        selected_option = (selected_option + 1) % 2  # Alterna entre Start Over y Quit

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_option == 0:
                            game.game_over = False
                            game.reset()
                        elif selected_option == 1:
                            main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.game_over = False
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()

        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))

            RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 490),
                                    text_input="Start Over", font=get_font(17),
                                    base_color=Colors.orange if selected_option == 0 else Colors.white,
                                    hovering_color=Colors.orange)

            QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 565),
                                text_input="QUIT", font=get_font(17),
                                base_color=Colors.orange if selected_option == 1 else Colors.white,
                                hovering_color=Colors.dark_blue)

            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)


        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def medium():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Medium Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,250)

    selected_option = 0  # 0 = Start Over, 1 = Quit
    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Movimiento con teclado
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_SPACE:
                    game.rotate()

            # Movimiento con D-Pad del control
            if event.type == pygame.JOYHATMOTION and not game.game_over:
                hat_x, hat_y = event.value
                if hat_x == -1:
                    game.move_left()
                elif hat_x == 1:
                    game.move_right()
                if hat_y == -1:
                    game.move_down()
                    game.update_score(0, 1)


            # Botón A del mando para rotar (button 0)
            if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                if event.button == 0:
                    game.rotate()

            # Timer automático
            if event.type == game_update and not game.game_over:
                game.move_down()

# Movimiento en Game Over
            if game.game_over:
                if event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = event.value
                    if hat_y == -1 or hat_y == 1:
                        selected_option = (selected_option + 1) % 2  # Alterna entre Start Over y Quit

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_option == 0:
                            game.game_over = False
                            game.reset()
                        elif selected_option == 1:
                            main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.game_over = False
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()

        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))

            RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 490),
                                    text_input="Start Over", font=get_font(17),
                                    base_color=Colors.orange if selected_option == 0 else Colors.white,
                                    hovering_color=Colors.orange)

            QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 565),
                                text_input="QUIT", font=get_font(17),
                                base_color=Colors.orange if selected_option == 1 else Colors.white,
                                hovering_color=Colors.dark_blue)

            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)

        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def hard():
    score_surface = get_font(17).render("Score", True, Colors.white)
    next_surface = get_font(17).render("Next", True, Colors.white)
    gameover_surface = get_font(25).render("Game Over", True, Colors.white)

    score_rect = pygame.Rect(950,55,170,60)
    next_rect = pygame.Rect(950,200,170,165)
  
    pygame.display.set_caption("Game - Hard Mode")

    clock = pygame.time.Clock()

    game = Game()

    game_update = pygame.USEREVENT
    pygame.time.set_timer(game_update,150)
    selected_option = 0  # 0 = Start Over, 1 = Quit
    while True:                                  
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface, (993,20,50,50))
        screen.blit(next_surface, (1000,165,50,35))
        score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Teclado (opcional mantener)
            if event.type == pygame.KEYDOWN and not game.game_over:
                if event.key == pygame.K_LEFT:
                    game.move_left()
                if event.key == pygame.K_RIGHT:
                    game.move_right()
                if event.key == pygame.K_DOWN:
                    game.move_down()
                    game.update_score(0, 1)
                if event.key == pygame.K_SPACE:
                    game.rotate()

            # D-Pad del joystick
            if event.type == pygame.JOYHATMOTION and not game.game_over:
                hat_x, hat_y = event.value
                if hat_x == -1:
                    game.move_left()
                elif hat_x == 1:
                    game.move_right()
                if hat_y == -1:
                    game.move_down()
                    game.update_score(0, 1)
                if hat_y == 1:
                    game.rotate()  # Opcional: rotación también con arriba

            # Botón A (button 0) para rotar pieza
            if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                if event.button == 0:
                    game.rotate()

            # Avance automático de pieza
            if event.type == game_update and not game.game_over:
                game.move_down()


# Movimiento en Game Over
            if game.game_over:
                if event.type == pygame.JOYHATMOTION:
                    hat_x, hat_y = event.value
                    if hat_y == -1 or hat_y == 1:
                        selected_option = (selected_option + 1) % 2  # Alterna entre Start Over y Quit

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_option == 0:
                            game.game_over = False
                            game.reset()
                        elif selected_option == 1:
                            main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESTART_BUTTON.checkForInput(mouse_pos):
                        game.game_over = False
                        game.reset()
                    if QUIT_BUTTON.checkForInput(mouse_pos):
                        main_menu()


        if game.game_over == True:
            screen.blit(gameover_surface, (927,415,50,35))

            RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 490),
                                    text_input="Start Over", font=get_font(17),
                                    base_color=Colors.orange if selected_option == 0 else Colors.white,
                                    hovering_color=Colors.orange)

            QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1039, 565),
                                text_input="QUIT", font=get_font(17),
                                base_color=Colors.orange if selected_option == 1 else Colors.white,
                                hovering_color=Colors.dark_blue)

            for button in [RESTART_BUTTON, QUIT_BUTTON]:
                button.changeColor(mouse_pos)
                button.update(screen)


        pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
        game.draw(screen)
            
        pygame.display.update()
        clock.tick(60)

def main_menu():
    selected_index = 0  # 0 = EASY, 1 = MEDIUM, 2 = HARD, 3 = EXIT
    options = ["EASY", "MEDIUM", "HARD", "EXIT"]

    while True:
        screen.blit(BG, (0, 0))
        menu_surface = get_font(100).render("TETRIS", True, "#b68f40")
        menu_rect = menu_surface.get_rect(center=(640, 100))
        screen.blit(menu_surface, menu_rect)

        buttons = [
            Button(image=pygame.image.load(current_dir + "/assets/Play Rect.png"), pos=(640, 230), 
                   text_input="EASY", font=get_font(40), base_color=Colors.white, hovering_color=Colors.green),
            Button(image=pygame.image.load(current_dir + "/assets/Medium Rect.png"), pos=(640, 350), 
                   text_input="MEDIUM", font=get_font(40), base_color=Colors.white, hovering_color=Colors.purple),
            Button(image=pygame.image.load(current_dir + "/assets/Play Rect.png"), pos=(640, 470), 
                   text_input="HARD", font=get_font(40), base_color=Colors.white, hovering_color=Colors.red),
            Button(image=pygame.image.load(current_dir + "/assets/Exit Rect.png"), pos=(640, 590), 
                   text_input="EXIT", font=get_font(40), base_color=Colors.white, hovering_color=Colors.dark_blue),
        ]

        for i, button in enumerate(buttons):
            if i == selected_index:
                button.base_color = Colors.orange  # Opción seleccionada
            else:
                button.base_color = Colors.white
            button.changeColor(pygame.mouse.get_pos())  # Para que también siga funcionando con mouse
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].checkForInput(pygame.mouse.get_pos()):
                    easy()
                if buttons[1].checkForInput(pygame.mouse.get_pos()):
                    medium()
                if buttons[2].checkForInput(pygame.mouse.get_pos()):
                    hard()
                if buttons[3].checkForInput(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

            # D-Pad
            if event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = event.value
                if hat_y == 1:  # Arriba
                    selected_index = (selected_index - 1) % len(options)
                if hat_y == -1:  # Abajo
                    selected_index = (selected_index + 1) % len(options)

            # Botón A
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    if selected_index == 0:
                        easy()
                    elif selected_index == 1:
                        medium()
                    elif selected_index == 2:
                        hard()
                    elif selected_index == 3:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


main_menu()