import pygame as pg
import config as cfg
import Maze_Gen as MG

class Game():
    def __init__(self):
        pg.init()

        self.config = cfg.Config()

        self.screen = pg.display.set_mode(self.config.resolution)

        self.maze = MG.Maze(self, (20,10), 12345)

        print(f"maze layout:")
        for row in self.maze.layout:
            print(f"{row}\n")

        print(f"maze board:")
        for row in self.maze.board:
            print(f"{row}\n")

        while True:
            self.maze.all_sprites.draw(self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return


Game()