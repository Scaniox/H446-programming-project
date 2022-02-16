import pygame as pg

colours = [(0xAC, 0x32, 0x32),
            (0xDF, 0x71, 0x26),
            (0x99, 0XE5, 0X50),
            (0X00, 0X50, 0xEF),
            (0X76, 0X42, 0X8A),
            (0X00, 0XCC, 0XCC)]


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
        self.colour = [round(i) for i in colours[colour]]
        super().__init__(game, start_pos)

class Block(Parent):
    def __init__(self, game, start_pos, colour):
        self.colour = [round(i*0.6) for i in colours[colour]]
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
