import pygame
import random
import os
from os import path
FPS = 60
WIDTH = 480
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


os.environ['SDL_VIDEO_CENTERED'] = '1' #place window in the center of the monitor
 

img_dir = path.join(path.dirname(__file__), "img")
sound_dir = path.join(path.dirname(__file__), "sound")
font_name = pygame.font.match_font("arial")



#define functions
def first_level():
	for i in range(6):
		random_x = random.randrange(20, WIDTH - 20)
		random_y = random.randrange(-150, -50)
		e = EnemySpaceShip(random_x, random_y)
		all_sprites.add(e)
		enemy_spaceships.add(e)
		
def second_level():
	first_level()
	random_x1 = random.randrange(-300, -250)
	random_y1 = random.randrange(100, HEIGHT - 100)
	random_x2 = random.randrange(WIDTH + 250, WIDTH + 300)
	random_y2 = random.randrange(100, HEIGHT - 100)
	e1 = Ufo(random_x1, random_y1, "ufo_from_left")
	e2 = Ufo(random_x2, random_y2, "ufo_from_right")
	all_sprites.add(e1)
	all_sprites.add(e2)
	enemy_spaceships.add(e1)
	enemy_spaceships.add(e2)

def third_level():
	pass
		
def draw_text (surface, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, WHITE) # True allows us to use Anti-aliased text on this surface
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surface.blit(text_surface, text_rect)




#define classes
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50, 38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.speed = 5
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		
	def update(self):
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.rect.x -= self.speed
		if keystate[pygame.K_RIGHT]:
			self.rect.x += self.speed
		if keystate[pygame.K_UP]:
			self.rect.y -= self.speed
		if keystate[pygame.K_DOWN]:
			self.rect.y += self.speed
		if keystate[pygame.K_SPACE]:
			self.shoot()
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
	
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet("player", self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			player_bullets.add(bullet)
			shoot_sound.play()

class Bullet (pygame.sprite.Sprite):
	def __init__(self,type, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.type = type
		if self.type == "player":
			self.image = bullet_img
			self.speed = 10
		elif self.type == "enemy":
			self.image = pygame.transform.rotate(enemy_bullet_img, 180)
			self.speed = 8
		elif self.type == "ufo_right":
			self.image = pygame.transform.rotate(ufo_bullet_img, 270)
			self.speed = 8
		elif self.type == "ufo_left":
			self.image = pygame.transform.rotate(ufo_bullet_img, 90)
			self.speed = 8
		elif self.type == "ufo_top":
			self.image = ufo_bullet_img
			self.speed = 8
		elif self.type == "ufo_bottom":
			self.image = pygame.transform.rotate(ufo_bullet_img, 180)
			self.speed = 8
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.centerx = x
		
		
	def update(self):
		if self.type == "player":
			self.rect.y -= self.speed
		elif self.type == "enemy":
			self.rect.y += self.speed
		elif self.type == "ufo_right":
			self.rect.right += self.speed
		elif self.type == "ufo_left":
			self.rect.left -= self.speed
		elif self.type == "ufo_top":
			self.rect.top -= self.speed
		elif self.type == "ufo_bottom":
			self.rect.bottom += self.speed
		if (self.rect.bottom < 0 and (self.type ==  "player" or self.type == "ufo_top")) or (self.rect.top > HEIGHT and (self.type == "enemy" or self.type == "ufo_bottom")) or (self.rect.left > WIDTH and self.type == "ufo_right") or (self.rect.right < 0 and self.type == "ufo_left"):
			self.kill()
			
		
			

class EnemySpaceShip(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(enemy_spaceship_img, (53, 40))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = y
		self.speed = 3
		self.maximum_elevation = random.randrange(200, 400)
		self.direction = random.random()
		self.direction_counter = 0
		self.last_shot = pygame.time.get_ticks()
		self.shoot_delay = random.randrange(500, 1200)
		self.is_arrived = False
	
	def update(self):
		if self.rect.top > 30:
			self.is_arrived = True
		if self.is_arrived:
			if self.direction_counter > 10:
				self.direction = random.random()
				self.direction_counter = 0
				self.shoot()
			if 0 < self.direction < 0.3: #go left
				self.rect.left -= self.speed
			elif 0.3 <  self.direction < 0.6: #go right
				self.rect.right += self.speed
			elif 0.6 <  self.direction < 0.8: #go down
				self.rect.bottom += self.speed
			elif 0.9 < self.direction < 1.00: #go up
				self.rect.top -= self.speed
			
			self.direction_counter += 1
		else:
			self.rect.bottom += self.speed
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > self.maximum_elevation:
			self.rect.bottom = self.maximum_elevation
	
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet("enemy", self.rect.centerx, self.rect.bottom)
			all_sprites.add(bullet)
			enemy_bullets.add(bullet)
			enemy_shoot_sound.play()


class Explosion (pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_animation[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50
		
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_animation[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_animation[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

class Ufo (pygame.sprite.Sprite):
	def __init__ (self, x, y, type):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(ufo_img, (60,60))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.top = y
		self.speed = 2
		self.is_arrived = False
		self.direction = random.random()
		self.direction_counter = 0
		self.last_shot = pygame.time.get_ticks()
		self.shoot_delay = random.randrange(2000, 3000)
		self.type = type
	
	def update(self):
		if self.rect.left >80 and self.rect.right < WIDTH - 80:
			self.is_arrived = True
		if self.is_arrived:
			if self.direction_counter > 20:
				self.direction = random.random()
				self.direction_counter = 0
				self.shoot()
			if 0 < self.direction < 0.3: #go left
				self.rect.left -= self.speed
			elif 0.3 <  self.direction < 0.6: #go right
				self.rect.right += self.speed
			elif 0.6 <  self.direction < 0.7: #go down
				self.rect.bottom += self.speed
			elif 0.7 < self.direction < 0.8: #go up
				self.rect.top -= self.speed
			
			self.direction_counter += 1
		else:
			if self.type == "ufo_from_left":
				self.rect.right += self.speed
			elif self.type == "ufo_from_right":
				self.rect.left -= self.speed
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
	
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet_right = Bullet("ufo_right", self.rect.centerx, self.rect.centery)
			bullet_left = Bullet("ufo_left", self.rect.centerx, self.rect.centery)
			bullet_top = Bullet("ufo_top", self.rect.centerx, self.rect.centery)
			bullet_bottom = Bullet("ufo_bottom", self.rect.centerx, self.rect.centery)
			all_sprites.add(bullet_right)
			all_sprites.add(bullet_left)
			all_sprites.add(bullet_top)
			all_sprites.add(bullet_bottom)
			enemy_bullets.add(bullet_right)
			enemy_bullets.add(bullet_left)
			enemy_bullets.add(bullet_top)
			enemy_bullets.add(bullet_bottom)
			ufo_shoot_sound.play()	


#initialize pygame and create window
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

#load all game graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_orange.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue07.png")).convert()
enemy_spaceship_img = pygame.image.load(path.join(img_dir, "spaceShips_001.png")).convert()
enemy_bullet_img = pygame.image.load(path.join(img_dir, "laserRed07.png")).convert()
ufo_bullet_img = pygame.image.load(path.join(img_dir, "lasergreen11.png")).convert()
ufo_img = pygame.image.load(path.join(img_dir, "ufoGreen.png")).convert()
background_rect = background.get_rect()
explosion_animation = {}
explosion_animation["large"] = []
explosion_animation["player"] = []
for i in range(9):
	file_name = "regularExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, file_name)).convert()
	img.set_colorkey(BLACK)
	large_img = pygame.transform.scale(img, (75, 75))
	explosion_animation["large"].append(large_img)
	file_name = "sonicExplosion0{}.png".format(i)
	img = pygame.image.load(path.join(img_dir, file_name)).convert()
	img.set_colorkey(BLACK)
	explosion_animation["player"].append(img)
	

#load all game sounds
pygame.mixer.music.load(path.join(sound_dir, "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops = -1)
shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "pew.wav"))
enemy_shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "enemy_pew.wav"))
death_explosion_sound = pygame.mixer.Sound(path.join(sound_dir, "rumble1.ogg"))
ufo_shoot_sound = pygame.mixer.Sound(path.join(sound_dir, "alien_device_0.wav"))
explosion_sounds = []
for sound in ["explosion1.wav", "explosion2.wav"]:
	explosion_sound = pygame.mixer.Sound(path.join(sound_dir, sound))
	explosion_sounds.append(explosion_sound)
	explosion_sound.set_volume(0.3)
shoot_sound.set_volume(0.6)
enemy_shoot_sound.set_volume(0.3)
ufo_shoot_sound.set_volume(0.4)

#create all the objects
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
enemy_spaceships = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
current_level = 1




first_level()

#game loop
running = True
while running:
	#keep loop running at the right speed
	clock.tick(FPS)
	#process input
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	hits = pygame.sprite.groupcollide(player_bullets, enemy_spaceships, True, True)
	for hit in hits:
		explosion = Explosion(hit.rect.center, "large")
		all_sprites.add(explosion)
		random.choice(explosion_sounds).play()
	hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
	for hit in hits:
		death_explosion = Explosion(hit.rect.center, "player")
		all_sprites.add(death_explosion)
		death_explosion_sound.play()
		player.kill()
	if  not player.alive() and not death_explosion.alive():	
		running = False
		timer = 0
	if len(enemy_spaceships) == 0 and current_level == 1:
		current_level = 2
		second_level()
	elif len(enemy_spaceships) == 0 and current_level == 2:
		current_level = 3
		third_level() 
		
		

	#update
	all_sprites.update()

	#draw/render
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, "Level: " + str(current_level), 18, WIDTH/2, 10)
	pygame.display.flip()
pygame.quit()
	
	
	
	
			
