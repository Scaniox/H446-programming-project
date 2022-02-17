from tracemalloc import start
import pygame as pg

vec2 = pg.math.Vector2


class Renderable_Sprite(pg.sprite.Sprite):
    def __init__(self, game, start_pos=(0,0), start_rot=0):
        super().__init__()

        # initialise 
        self.game = game
        self.camera = self.game.level.camera
        self.pos = vec2(start_pos)
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
        self.vel = vec2(0,0)
        # set max speed 
        self.max_speed = game.config.player_max_speed
        # set acc
        self.acc = game.config.player_acc
        
        # animations
        self.animation_state = "standing"
        # load animation frames
        self.standing_imgs = 

        self.walking_imgs = 

        # sounds
        self.key_collect_snd = self.game.snd_loader.get("key collect.wav")

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
            self.vel.x -= self.acc
            walking = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            # acc right
            self.vel.x += self.acc
            walking = True
        
        if keys[pg.K_UP] or keys[pg.K_w]:
            # acc up
            self.vel.y -= self.acc
            walking = True
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            # acc down
            self.vel.y += self.acc
            walking = True

        # enforce max speed
        self.vel = [min(max(-self.max_speed, self.vel[i]), self.max_speed) \
                    for i in (0,1)]

        # decelerate back to vel = 0 if not walking
        if not walking:
            speed = max(self.vel.length, 1e-15)
            self.vel -= [ min(self.acc * self.vel[i]/speed, self.vel[i])
                          for i in (0,1)]

        # block picking and placing
        slot_keys = [keys[pg.K_q], keys[pg.K_e]]
        for slot_index in (0,1):
            if slot_keys[slot_index]:
                # if the slot is empty, pick up
                if self.inventory[slot_index] == False:
                    self.pick_up(slot_index)
                # if slot is full, place
                else:
                    self.place(slot_index)

        # collisions with keys
        hits = pg.sprite.spritecollide(self, self.game.level.maze.keys, True)
        self.keys += len(hits)
        if len(hits):
            self.key_collect_snd.play()

        # update rot based on movement
        self.rot = self.vel.angle_to(vec2(0,1))

        # collide with walls
        self.collide()

        # respawn
        if self.health == 0:
            self.respawn()

    def pick_up(self, slot_index):
        """picks up block in front of the player and stores in inventory"""


        

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
        self.pos = vec2(0,0) # this location is the centre of the screen
        self.target = target
        self.zoom = self.game.config.camera_zoom
    
    def update(self, dt):
        """updates the position of the camera so that it tracks the player"""

        # adjust the camera pos
        target_pos = vec2(self.target.pos)
        target_pos_delta = target_pos - self.pos
        self.pos = self.pos - 0.1*target_pos_delta

        # ensure camera never goes of screen
        unscaled_scrn_size = vec2(self.game.config.resolution)/ self.zoom
        wrld_size = self.game.level.maze.bsize

        left_edge = unscaled_scrn_size.x/2
        right_edge = wrld_size.x - unscaled_scrn_size.x/2
        top_edge = unscaled_scrn_size.y/2
        bottom_edge = wrld_size.y - unscaled_scrn_size.y/2

        self.pos.x = min(max(left_edge, self.pos.x), right_edge)
        self.pos.y = min(max(top_edge, self.pos.y), bottom_edge)

    def wrld_2_scrn_coord(self, wrld_coord):
        """takes a world space coordinate and converts it to screenspace"""
        scrn_size = vec2(self.game.config.resolution)

        # ensures that the cameras position ends up at the centre of the screen
        scaled_wrld_coord = vec2(wrld_coord) * self.zoom
        scaled_pos = self.pos * self.zoom
        ss_coord = scaled_wrld_coord + scrn_size/2 - scaled_pos
        return ss_coord