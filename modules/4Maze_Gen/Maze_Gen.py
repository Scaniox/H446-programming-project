import pygame as pg
import random as rng
import Sprites_dummy as Sprites

class Maze():
    def __init__(self, game, msize, seed):
        # store maze size and seed
        self.game = game
        self.msize = msize
        self.seed = seed

        # initialise RNG
        rng.seed(self.seed)

        # generate maze layout
        self.generate_layout()

        # convert layout to wall sprites
        wall_gen = lambda pos: Sprites.Wall(self.game, pos)
        self.layout_to_board(wall_gen)

        # find start to end path
        self.start_to_end_path = self.get_shortest_path(self.start, self.end)

        # populate

    def generate_layout(self):
        # uses kruskal's algorithm to generate maze layout

        # store layout to attribute

        # generate start

        # generate end

    def layout_to_board(self, wall_gen):
        # generate board array

        # place corner sprites on board

        # place edge sprites on board

        # uses wall generator to generate walls from board and store

    def populate(self):
        # populate keys

        # populate checkpoints

        # populate enemies

    def get_shortest_path(self, start, end):
        # dijkstra's algorithm
