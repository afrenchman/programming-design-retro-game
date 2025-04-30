import pygame,sys
import random
import os
import main 

pygame.init()

class Colors:
    dark_grey = (26,31,40)
    green = (47,230,23)
    red = (232,18,18)
    orange = (226,116,17)
    yellow = (237,234,4)
    purple = (166,0,247)
    cyan = (21,204,209)
    blue = (13,64,216)
    white = (255,255,255)
    dark_blue = (44,44,127)
    light_blue = (59,85,162)
    black = (0,0,0)

    @classmethod
    def get_cell_colors(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
    
class Position:
    def __init__(self, row, column):
        self.row = row 
        self.column = column

class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size = 35
        self.row_offset = 0
        self.column_offset = 0
        self.rotation_state = 0
        self.colors = Colors.get_cell_colors()

    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state == len(self.cells):
            self.rotation_state = 0

    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1

    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pygame.Rect(offset_x + tile.column*self.cell_size, offset_y + tile.row*self.cell_size, self.cell_size - 1, self.cell_size - 1)
            pygame.draw.rect(screen, self.colors[self.id], tile_rect)

class Lblock(Block):
    def __init__(self):
        super().__init__(id = 1)
        self.cells = {
            0: [Position(0,2), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(2,1), Position(2,2)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,0)],
            3: [Position(0,0), Position(0,1), Position(1,1), Position(2,1)],
        }
        self.move(0,3)

class Jblock(Block):
    def __init__(self):
        super().__init__(id = 2)
        self.cells = {
            0: [Position(0,0), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(0,2), Position(1,1), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,2)],
            3: [Position(0,1), Position(1,1), Position(2,0), Position(2,1)],
        }
        self.move(0,3)

class Iblock(Block):
    def __init__(self):
        super().__init__(id = 3)
        self.cells = {
            0: [Position(1,0), Position(1,1), Position(1,2), Position(1,3)],
            1: [Position(0,2), Position(1,2), Position(2,2), Position(3,2)],
            2: [Position(2,0), Position(2,1), Position(2,2), Position(2,3)],
            3: [Position(0,1), Position(1,1), Position(2,1), Position(3,1)],
        }
        self.move(-1,3)

class Oblock(Block):
    def __init__(self):
        super().__init__(id = 4)
        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,0), Position(1,1)],
        }
        self.move(0,4)

class Sblock(Block):
    def __init__(self):
        super().__init__(id = 5)
        self.cells = {
            0: [Position(0,1), Position(0,2), Position(1,0), Position(1,1)],
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,2)],
            2: [Position(1,1), Position(1,2), Position(2,0), Position(2,1)],
            3: [Position(0,0), Position(1,0), Position(1,1), Position(2,1)],
        }
        self.move(0,3)

class Tblock(Block):
    def __init__(self):
        super().__init__(id = 6)
        self.cells = {
            0: [Position(0,1), Position(1,0), Position(1,1), Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(1,2), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2), Position(2,1)],
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,1)],
        }
        self.move(0,3)

class Zblock(Block):
    def __init__(self):
        super().__init__(id = 7)
        self.cells = {
            0: [Position(0,0), Position(0,1), Position(1,1), Position(1,2)],
            1: [Position(0,2), Position(1,1), Position(1,2), Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(2,1), Position(2,2)],
            3: [Position(0,1), Position(1,0), Position(1,1), Position(2,0)],
        }
        self.move(0,3)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color = base_color
		self.hovering_color = hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

current_dir = os.path.dirname(os.path.abspath(__file__))

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.rotate_sound = pygame.mixer.Sound(current_dir + "/sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound(current_dir + "/sounds/clear.ogg")

        pygame.mixer.music.load(current_dir + "/sounds/tetris_soundtrack.mp3")
        pygame.mixer.music.play(-1)

    def update_score(self, rows_cleared, move_down_points):
        if rows_cleared == 1:
            self.score += 50
        elif rows_cleared == 2:
            self.score += 120
        elif rows_cleared == 3:
            self.score += 300
        elif rows_cleared == 4:
            self.score += 500
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0,-1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,1)

    def move_right(self):
        self.current_block.move(0,1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0,-1)

    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1,0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 600, 170)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 1111, 465)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 1111, 445)
        else:   
            self.next_block.draw(screen, 1129, 445)

class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 35
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors()

    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    def is_inside(self, row, column):
        if row >= 0 and row < self.num_rows and column >= 0 and column < self.num_cols:
            return True
        return False
    
    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_full(self, row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self, row):
        for column in range(self.num_cols):
            self.grid[row][column] == 0

    def move_row_down(self, row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1, 0, -1):
            if self.is_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0

    def draw(self, screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pygame.Rect(column*self.cell_size + 600, row*self.cell_size + 170, self.cell_size - 1, self.cell_size - 1)
                pygame.draw.rect(screen, self.colors[cell_value], cell_rect)

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
	
    run = True

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

        while run:                                  
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

        while run:                                  
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

        while run:                                  
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

        while run:
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
                            run = False
                            main.main()

            pygame.display.update()

    main_menu()

if __name__ == "__main__":
    os.environ['SDL_VIDEO_CENTERED'] = '1' 
    pygame.init()
    tetris_play()
    pygame.quit()
