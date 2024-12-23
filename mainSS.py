# This file was created by: James Castelly 

# IMPORT ALL NECESSARY MODULES AND LIBRARIES
import pygame as pg
from settingsSS import *
from spritesSS import *
from tilemap import *
from os import path
from random import randint
import sys
from utils import *
'''
GOALS: Survive for as long as possible
RULES: Get powerups to speed up and avoid the mobs but watch out for fakepowerups!
FEEDBACK: If you collide with an enemy 3 times you die
FREEDOM: Move around inside the game space

What sentence does your game make? 



'''''

'''
Sources: 

'''



# created a game class to instantiate later
# it will have all the necessary parts to run the game
# the game class is created to organize the elements needed to create a gam 
class Game:
    # The game init method initializes all the necessary components for the game, including video and sound
    # this includes the game clock which allows us to set the framerate
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("James' Game")
        self.clock = pg.time.Clock()
        self.running = True
        self.score = 0
    # create player block, creates the all_sprites group so that we can batch update and render, defines properties that can be seen in the game system
    #
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
        #     f.write(str(0))
        try:
            with open(path.join(self.game_folder, HS_FILE), 'r') as f:
                self.highscore = int(f.read())
        except:
            self.highscore = 0
            with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                f.write(str(self.highscore))
   
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, 'level2.txt'))
    def new(self):
        self.load_data()
        print(self.map.data)
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.all_powerups = pg.sprite.Group()
        self.all_coins = pg.sprite.Group()
        # self.player = Player(self, 1, 1)
        # instantiated a mob
        # self.mob = Mob(self, 100,100)
        # makes new mobs and walls using a for loop
        # for i in range(randint(10,20)):
        #     m = Mob(self, i*randint(0, 200), i*randint(0, 200))
        #     Wall(self, i*TILESIZE, i*TILESIZE)
        

        # takes map.data and parses it using enumerate so that we can assign x and y values to 
        # object instances.
        for row, tiles in enumerate(self.map.data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'U':
                    Powerup(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'H':
                    FakePowerup(self, col, row)
    # using self.running as a boolean to continue running the game
    def run(self):
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
        # input
    def quit(self):
        pg.quit()
        sys.exit()
    # Looks for any events, and this specifically looks for closing the game with 'x'
    def events(self):
        for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.score > self.highscore:
                        with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                            f.write(str(self.score))
                    self.running = False

        # pg.quit()
        # process
    def update(self):
        if self.player.lives == 0:
            self.show_death_screen()
            self.running = False
            self.timer.ticking()
        # what to do when the player runs out of lives
        if self.player.lives == 0:
            if self.score > self.highscore:
                    with open(path.join(self.game_folder, HS_FILE), 'w') as f:
                      f.write(str(self.score))
            self.show_death_screen()
            self.running = False
 
        if self.score >= 300 and not self.extra_life_spawned:
            self.spawn_life_powerup(WIDTH//2, 0)
            self.extra_life_spawned = True
            
        self.all_sprites.update()
        self.playing = False
        # output
    
    def show_start_screen(self):
        self.load_data()
        if not self.running:
            return
        self.screen.fill(BLACK)
        self.draw_text(self.screen, "Welcome! ", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text(self.screen, "Best time: " + str(self.best_time), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text(self.screen, "Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        self.screen.fill(WHITE)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "lives:" + str(self.player.lives) , 24, WHITE, WIDTH -32, HEIGHT -32)
        self.draw_text(self.screen, "Score:" + str(self.score), 24, BLACK, 96, 32)
        #self.draw_text(self.screen, "Highscore:" + str(self.highscore), 24, BLACK, WIDTH/2, 32)
        pg.display.flip()
    def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You're Trash!", 42, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

def show_death_screen(self):
        self.screen.fill(RED)
        self.draw_text(self.screen, "You Died!", 42, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
 
def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

# checks file name and creates a game object
if __name__ == "__main__":
    g = Game()
    # create all game elements with the new method (not function)
    g.new()
    # run the game
    g.run()

        