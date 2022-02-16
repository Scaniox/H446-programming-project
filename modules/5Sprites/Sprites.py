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
        # call parent constructor
        super().__init__(game, start_pos, 0)

        self.colour = game.config.colours[0]
        # set health
        self.health = game.config.player_max_health
        # set hurt cooldown
        self.hurt_cooldown = game.config.player_hurt_cooldown

        # kinematics
        self.vel = (0, 0)
        # set max speed 
        self.max_speed = game.config.player_max_speed
        # set acc
        self.acc = game.config.player_acc
        
        # animations
        self.animation_state = "standing"
        # load animation frames
        self.standing_imgs = 

        self.walking_imgs = 

        # set up other mechanics
        self.inventory = [False, False]
        self.keys = 0
        self.last_checkpoint = False

    def update(self, dt):
        # acceleration due to wasd
        keys = pg.key.get_pressed()
        walking = False
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # acc left
            self.vel[0] -= self.acc
            walking = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            # acc right
            self.vel[0] += self.acc
            walking = True
        
        if keys[pg.K_UP] or keys[pg.K_w]:
            # acc up
            self.vel[1] -= self.acc
            walking = True
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            # acc down
            self.vel[1] += self.acc
            walking = True

        if not walking:
            speed = max((self.vel[0]**2 + self.vel[1]**2)**(1/2), 1e-15)
            self.vel -= [ self.acc * self.vel[i]/speed  for i in (0,1)]
        

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