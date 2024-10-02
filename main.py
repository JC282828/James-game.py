# this file was created by: James Castelly

# this is where we import libraries and modules
import pygame as pg
from settings import *
from sprites import *
# we are editing this file after installing git

# create a game class that carries all the properties of the game and methods
class Game:
  def __init__(self):
    pg.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    # pg.display.set_caption("James' Game")
    self.playing = True
    #If this is turned false, it will not start no matter what
  # this is where the game creates the things you see and hear
  def new(self):
    # create sprite group using the pg library
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    # instantiating the class to create the player object 
    self.player = Player(self, 5, 5)
    self.mob = Mob(self, 100, 100)
    self.wall = Wall(self, WIDTH//2, HEIGHT//2)

    for i in range(6):
      w = Wall(self, TILESIZE*i, TILESIZE*i)
      print(w.rect.x)
      m = Mob(self, TILESIZE*i, TILESIZE*i)

# this is a method
# methods are like functions that are part of a class
# the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites...and I MEAN ALL OF THEM
    self.all_sprites.update()

  # output
  def draw(self):
    self.screen.fill((0, 0, 0))
    self.all_sprites.draw(self.screen)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running")
  g = Game()
  print("main is running")
  g.new()
  #Start your Engines
  g.run()
  #GO!
  