import os
import random
import sys
import pygame
from settings import *
from sprites import *
from camera import *
from graphics import *

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
