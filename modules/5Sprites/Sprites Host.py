import config as cfg
import Maze_Gen as mg
import Asset_Loader as al
import pygame as pg
import Sprites as sprites
import random as rng

class Game():
    def __init__(self):
        # init pygame
        pg.init()
        
        # config
        self.config = cfg.Config()
        
        # init screen
        self.screen = pg.display.set_mode(self.config.resolution)

        # init asset loaders
        self.img_loader = al.Img_Loader(self)
        self.snd_loader = al.Snd_Loader(self)

        # run level level
        self.level = Level(self)
        self.level.setup()
        self.level.loop()

class Level():
    def __init__(self, game):
        self.game = game
        self.timer = sprites.Timer(self.game)

    def setup(self):
        """sets up the level"""
        # initialise camera
        self.camera = sprites.Camera(self.game)

        # start setting up the maze
        self.maze = mg.Maze(self.game, (20,10), rng.randint(0,10000))    
        # finishes generating the maze and sprites
        self.maze.setup()
        # initalise sprites in maze
        for sprite in self.maze.all_sprites:
                sprite.render(0)

        # initialise player
        self.player = sprites.Player(self.game, (self.maze.start))
        self.maze.all_sprites.add(self.player)
        # set what the camera should follow
        self.camera.set_target(self.player)
        self.camera.pos = pg.Vector2(5,5)

    def loop(self):

        clock = pg.time.Clock()
        while True:
            dt = clock.tick(75)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_t:
                        print(self.timer.total_time)
                    if event.key == pg.K_r:
                        self.timer.reset()

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.camera.zoom = min(self.camera.zoom+1, 20)
                    if event.button == 5:
                        self.camera.zoom = max(self.camera.zoom-1 , 1)
            
            # update all sprites
            self.maze.all_sprites.update(dt)
            self.camera.update(dt)
            self.timer.update(dt)

            # call all sprites render method
            for sprite in self.maze.all_sprites:
                sprite.render(dt)

            self.game.screen.fill((32,32,32))
            self.maze.all_sprites.draw(self.game.screen)

            for sprite in self.maze.all_sprites:
                pg.draw.rect(self.game.screen, (255,255,255), sprite.hit_rect, 1)

            pg.display.flip()
        

Game()
