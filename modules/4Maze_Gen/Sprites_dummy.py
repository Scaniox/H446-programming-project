import pygame as pg

class Parent(pg.sprite.Sprite):
    def __init__(self, game, start_pos):
        super().__init__()
        
        self.image = pg.surface.Surface((16,24))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = start_pos

class Wall(Parent):
    def __init__(self, game, start_pos):
        self.colour = (32,32,32)
        super().__init__(game, start_pos)

class Gateway(Parent):
    def __init__(self, game, start_pos, colour):
        self.colour = (0,0,192)
        super().__init__(game, start_pos)

class Block(Parent):
    def __init__(self, game, start_pos, colour):
        self.colour = (0,192,0)
        super().__init__(game, start_pos)

class Enemy(Parent):
    def __init__(self, game, start_pos):
        self.colour = (192,0,0)
        super().__init__(game, start_pos)

class Checkpoint(Parent):
    def __init__(self, game, start_pos):
        self.colour = (128,128,0)
        super().__init__(game, start_pos)

class Key(Parent):
    def __init__(self, game, start_pos):
        self.colour = (128,128,128)
        super().__init__(game, start_pos)

class Exit(Parent):
    def __init__(self, game, start_pos):
        self.colour = (192,192,192)
        super().__init__(game, start_pos)
