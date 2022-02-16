from tracemalloc import start
import pygame as pg


class Renderable_Sprite(pg.sprite.Sprite):
    def __init__(self, game, start_pos=(0,0), start_rot=0):
        super().__init__()

        # initialise 
        self.game = game
        self.camera = self.game.level.camera
        self.pos = start_pos
        self.rot = start_rot

        # animations:
        self.imgs = []
        self.frame_index = 0
        self.frame_time = 100
        self.frame_countdown = 0
        
    def update(self, dt):
        pass

    def render(self, dt):
        # decrease frame_countdown 
        self.frame_countdown -= dt
        # advance to next frame if less than 0
        if self.frame_countdown < 0:
            self.frame_countdown = self.frame_time
            self.frame_index = (self.frame_index + 1) % len(self.imgs) 

        # retrieve correct img from imgs
        self.image = self.imgs[self.frame_index]

        # rotate image 
        self.image = pg.transform.rotate(self.image, self.rot)
        
        # set rect position correctly
        self.rect = self.image.get_rect()
        screen_pos = self.camera.wrld_2_scrn_coord(self.pos)
        self.rect.topleft = screen_pos


class Player(Renderable_Sprite):
    def _init__(self, game, start_pos):
        super().__init__(game, start_pos, 0)

class Enemy(Renderable_Sprite):
    def __init__(self, game, start_pos):
        self.colour = (192,0,0)
        super().__init__(game, start_pos)

class Wall(Renderable_Sprite):
    def __init__(self, game, start_pos):
        self.colour = (32,32,32)
        super().__init__(game, start_pos)


class Gateway(Renderable_Sprite):
    def __init__(self, game, start_pos, colour):
        self.colour = [round(i) for i in colours[colour]]
        super().__init__(game, start_pos)


class Block(Renderable_Sprite):
    def __init__(self, game, start_pos, colour):
        self.colour = [round(i*0.6) for i in colours[colour]]
        super().__init__(game, start_pos)


class Checkpoint(Renderable_Sprite):
    def __init__(self, game, start_pos):
        self.colour = (128,128,0)
        super().__init__(game, start_pos)


class Key(Renderable_Sprite):
    def __init__(self, game, start_pos):
        self.colour = (128,128,128)
        super().__init__(game, start_pos)


class Exit(Renderable_Sprite):
    def __init__(self, game, start_pos):
        self.colour = (192,192,192)
        super().__init__(game, start_pos)


class Camera():
    def __init__(self, game, target):
        self.pos = (0,0) # this location is the centre of the screen
        self.target = target
    
    def update(self, dt):
        """updates the position of the camera so that it tracks the player"""

        target_pos = self.target.pos
        # ensure camera never goes of screen
        scrn_size = self.game.config.resolution
        wrld_size = 

        left_edge = scrn_size[0]/2
        right_edge = wrld_size[0] - scrn_size[0]/2
        top_edge = scrn_size[1]/2
        bottom_edge = wrld_size[1] - scrn_size[1]/2

        # adjust the camera pos
        target_pos_delta = [target_pos[i] - self.pos[i] for i in (0,1)]
        self.pos = [round(self.pos[i] - 0.1*target_pos_delta[i]) for i in (0,1)]

    def wrld_2_scrn_coord(self, wrld_coord):
        """takes a world space coordinate and converts it to screenspace"""
        scrn_size = self.game.config.resolution
        # ensures that the cameras position ends up at the centre of the screen
        ss_coord = [wrld_coord[i] + scrn_size[i]/2 + self.pos for i in (0,1)]
        return ss_coord