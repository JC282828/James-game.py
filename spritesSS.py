# This file was created by: James Castelly

import pygame as pg
from pygame.sprite import Sprite
from settingsSS import *
import random 
from os import path

vec = pg.math.Vector2

class Player(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))
        self.rect = self.image.get_rect()
        self.image.fill(RED)
        # self.rect.x = x
        # self.rect.y = y
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.speed = 5
        # self.vx, self.vy = 0, 0
        self.jump_power = 19
        self.jumping = False
        self.lives = 3
    def get_keys(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.vy -= self.speed
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        # if keys[pg.K_s]:
        #     self.vy += self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            self.jump()
            print('BOINGGG')
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                    # self.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                    # self.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 2
                print ("I collided with a powerup")
                for m in self.game.all_mobs:
                    m.speed += 10
                    print("why are they getting faster?!")
                print("I've gotten a powerup!")       
            if str(hits[0].__class__.__name__) == "Fake Powerup":
                self.speed -= 90
                print("oof that hurt")
            if str(hits[0].__class__.__name__) == "Mob":
                self.lives -= 1
            if self.lives == 0 :
                pass
    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = - self.jump_power
    def update(self):
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        # self.x += self.vx * self.game.dt
        # self.y += self.vy * self.game.dt
        # reverse order to fix collision issues
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        
        # if abs(self.vel.x) < 0.1:
        #    self.vel.x = 0
        
        self.pos += self.vel + 0.5 * self.acc

        
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_mobs, True)
        self.collide_with_stuff(self.game.all_coins, True)

        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        
        self.rect.y = self.pos.y
        self.collide_with_walls('y')


class Mob(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs 
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((32, 32))  # Default size of the MOB
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)  # Default color for the MOB
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = random.choice([-2, 2])  # Initial random horizontal speed
        self.category = random.choice([0, 1])  # Category for future use

    def update(self):
        # Move MOB horizontally
        self.rect.x += self.speed

        # Check for collisions with walls
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits or self.rect.right > WIDTH or self.rect.left < 0:
            # Reverse direction when hitting a wall or screen edge
            self.speed *= 4
            self.rect.y += 32  # Move down when changing direction

        # Reset to the top if the mob reaches the bottom of the screen
        if self.rect.bottom > HEIGHT:
            self.reset_position()

    def reset_position(self):
        # Reset the MOB to the top of the screen
        self.rect.y = 0
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Randomize horizontal position
        self.speed = random.choice([-2, 2])  # Optionally reset speed


class Wall(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(BLUE)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def update(self):
        pass

class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(PINK)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(YELLOW)
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class FakePowerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINKISH)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
