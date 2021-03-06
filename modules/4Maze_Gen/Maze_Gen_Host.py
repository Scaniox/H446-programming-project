import pygame as pg
import config as cfg
import Maze_Gen as MG
import random

class Game():
    def __init__(self):
        pg.init()

        self.config = cfg.Config()

        self.screen = pg.display.set_mode(self.config.resolution)

        self.maze = MG.Maze(self, (20,10), random.randint(0, 10000))

        print(f"maze layout:")
        for row in self.maze.layout:
            print(f"{row}\n")

        print(f"maze board:")
        for row in self.maze.board:
            print(f"{row}\n")

        self.screen.fill((255,255,255))
        self.maze.all_sprites.draw(self.screen)
        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return


Game()