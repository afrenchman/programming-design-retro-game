import pygame,sys
from game import Game
from colors import Colors
from button import Button
import os
import main

pygame.init()

def tetris_play():
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Joystick connected: {joystick.get_name()}")
    else:
        joystick = None
        print("No joystick.")

    screen = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption("Tetris")

    current_dir = os.path.dirname(os.path.abspath(__file__))

    BG = pygame.image.load(current_dir + "/assets/background.jpg")

    def get_font(size): 
        return pygame.font.Font(current_dir + "/assets/font.ttf", size)

    def easy():
        score_surface = get_font(17).render("Score", True, Colors.white)
        next_surface = get_font(17).render("Next", True, Colors.white)
        gameover_surface = get_font(25).render("Game Over", True, Colors.white)

        score_rect = pygame.Rect(1200,200,170,60)
        next_rect = pygame.Rect(1200,400,170,165)
    
        pygame.display.set_caption("Game - Easy Mode")

        clock = pygame.time.Clock()

        game = Game()

        game_update = pygame.USEREVENT
        pygame.time.set_timer(game_update,230)

        selected_option = 0  # 0 = Start Over, 1 = Quit

        while True:                                  
            mouse_pos = pygame.mouse.get_pos()
            screen.fill(Colors.dark_blue)
            screen.blit(score_surface, (1243,160,50,50))
            screen.blit(next_surface, (1250,355,50,35))
            score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard 
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
                # Game controller
                if event.type == pygame.JOYHATMOTION and not game.game_over:
                    hat_x, hat_y = event.value
                    if hat_x == -1:
                        game.move_left()
                    elif hat_x == 1:
                        game.move_right()
                    if hat_y == -1:
                        game.move_down()
                        game.update_score(0, 1)
                if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                    if event.button == 0:
                        game.rotate()

                if event.type == game_update and game.game_over == False:
                    game.move_down()

                # Game Over
                if game.game_over:
                    # Game controller
                    if event.type == pygame.JOYHATMOTION:
                        hat_x, hat_y = event.value
                        if hat_y == -1 or hat_y == 1:
                            selected_option = (selected_option + 1) % 2  
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:
                            if selected_option == 0:
                                game.game_over = False
                                game.reset()
                            elif selected_option == 1:
                                main_menu()
                    # Mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESTART_BUTTON.checkForInput(mouse_pos):
                            game.game_over = False
                            game.reset()
                        if QUIT_BUTTON.checkForInput(mouse_pos):
                            main_menu()

            if game.game_over == True:
                screen.blit(gameover_surface, (1177,670,50,35))
                RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 750),
                                        text_input="Start Over", font=get_font(17),
                                        base_color=Colors.orange if selected_option == 0 else Colors.white,
                                        hovering_color=Colors.orange)
                QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 825),
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

        score_rect = pygame.Rect(1200,200,170,60)
        next_rect = pygame.Rect(1200,400,170,165)
    
        pygame.display.set_caption("Game - Easy Mode")

        clock = pygame.time.Clock()

        game = Game()

        game_update = pygame.USEREVENT
        pygame.time.set_timer(game_update,160)

        selected_option = 0  # 0 = Start Over, 1 = Quit

        while True:                                  
            mouse_pos = pygame.mouse.get_pos()
            screen.fill(Colors.dark_blue)
            screen.blit(score_surface, (1243,160,50,50))
            screen.blit(next_surface, (1250,355,50,35))
            score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard 
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
                # Game controller
                if event.type == pygame.JOYHATMOTION and not game.game_over:
                    hat_x, hat_y = event.value
                    if hat_x == -1:
                        game.move_left()
                    elif hat_x == 1:
                        game.move_right()
                    if hat_y == -1:
                        game.move_down()
                        game.update_score(0, 1)
                if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                    if event.button == 0:
                        game.rotate()

                if event.type == game_update and game.game_over == False:
                    game.move_down()

                # Game Over
                if game.game_over:
                    # Game controller
                    if event.type == pygame.JOYHATMOTION:
                        hat_x, hat_y = event.value
                        if hat_y == -1 or hat_y == 1:
                            selected_option = (selected_option + 1) % 2  
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:
                            if selected_option == 0:
                                game.game_over = False
                                game.reset()
                            elif selected_option == 1:
                                main_menu()
                    # Mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESTART_BUTTON.checkForInput(mouse_pos):
                            game.game_over = False
                            game.reset()
                        if QUIT_BUTTON.checkForInput(mouse_pos):
                            main_menu()

            if game.game_over == True:
                screen.blit(gameover_surface, (1177,670,50,35))
                RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 750),
                                        text_input="Start Over", font=get_font(17),
                                        base_color=Colors.orange if selected_option == 0 else Colors.white,
                                        hovering_color=Colors.orange)
                QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 825),
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

        score_rect = pygame.Rect(1200,200,170,60)
        next_rect = pygame.Rect(1200,400,170,165)
    
        pygame.display.set_caption("Game - Easy Mode")

        clock = pygame.time.Clock()

        game = Game()

        game_update = pygame.USEREVENT
        pygame.time.set_timer(game_update,100)

        selected_option = 0  # 0 = Start Over, 1 = Quit

        while True:                                  
            mouse_pos = pygame.mouse.get_pos()
            screen.fill(Colors.dark_blue)
            screen.blit(score_surface, (1243,160,50,50))
            screen.blit(next_surface, (1250,355,50,35))
            score_value_surface = get_font(20).render(str(game.score), True, Colors.white)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Keyboard 
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
                # Game controller
                if event.type == pygame.JOYHATMOTION and not game.game_over:
                    hat_x, hat_y = event.value
                    if hat_x == -1:
                        game.move_left()
                    elif hat_x == 1:
                        game.move_right()
                    if hat_y == -1:
                        game.move_down()
                        game.update_score(0, 1)
                if event.type == pygame.JOYBUTTONDOWN and not game.game_over:
                    if event.button == 0:
                        game.rotate()

                if event.type == game_update and game.game_over == False:
                    game.move_down()

                # Game Over
                if game.game_over:
                    # Game controller
                    if event.type == pygame.JOYHATMOTION:
                        hat_x, hat_y = event.value
                        if hat_y == -1 or hat_y == 1:
                            selected_option = (selected_option + 1) % 2  
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 0:
                            if selected_option == 0:
                                game.game_over = False
                                game.reset()
                            elif selected_option == 1:
                                main_menu()
                    # Mouse
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if RESTART_BUTTON.checkForInput(mouse_pos):
                            game.game_over = False
                            game.reset()
                        if QUIT_BUTTON.checkForInput(mouse_pos):
                            main_menu()

            if game.game_over == True:
                screen.blit(gameover_surface, (1177,670,50,35))
                RESTART_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 750),
                                        text_input="Start Over", font=get_font(17),
                                        base_color=Colors.orange if selected_option == 0 else Colors.white,
                                        hovering_color=Colors.orange)
                QUIT_BUTTON = Button(image=pygame.image.load(current_dir + "/assets/Restart Rect.png"), pos=(1289, 825),
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
            menu_surface = get_font(120).render("TETRIS", True, "#b68f40")
            menu_rect = menu_surface.get_rect(center=(950, 200))
            screen.blit(menu_surface, menu_rect)

            buttons = [
                Button(image=pygame.image.load(current_dir + "/assets/Easy Rect.png"), pos=(950, 350), 
                    text_input="EASY", font=get_font(50), base_color=Colors.white, hovering_color=Colors.green),
                Button(image=pygame.image.load(current_dir + "/assets/Medium Rect.png"), pos=(950, 470), 
                    text_input="MEDIUM", font=get_font(50), base_color=Colors.white, hovering_color=Colors.purple),
                Button(image=pygame.image.load(current_dir + "/assets/Hard Rect.png"), pos=(950, 590), 
                    text_input="HARD", font=get_font(50), base_color=Colors.white, hovering_color=Colors.red),
                Button(image=pygame.image.load(current_dir + "/assets/Exit Rect.png"), pos=(950, 710), 
                    text_input="EXIT", font=get_font(50), base_color=Colors.white, hovering_color=Colors.dark_blue),
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
                            main.main()

            pygame.display.update()

    main_menu()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1' 
    pygame.init()
    tetris_play()
    pygame.quit()
