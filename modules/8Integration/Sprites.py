import math
import random as rng
import time
from numpy import size
import pygame as pg

vec2 = pg.math.Vector2
colour_names = ["red", "orange", "green", "blue", "purple", "cyan"]

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)


class Renderable_Sprite(pg.sprite.Sprite):
    def __init__(self, game, start_pos=(0,0), start_rot=0):
        super().__init__()

        # initialise 
        self.game = game
        self.camera = self.game.level.camera
        self.pos = vec2(start_pos)
        self.rot = start_rot
        self.layer = int(self.pos.y)

        # animations:
        self.imgs = []
        self.frame_index = 0
        self.frame_time = 100
        self.frame_countdown = 0
        self.culling = True

        
    def update(self, dt):
        pass

    def render(self, dt):
        # decrease frame_countdown 
        self.frame_countdown -= dt
        # advance to next frame if less than 0
        if self.frame_countdown < 0:
            self.frame_countdown = self.frame_time
            self.frame_index = (self.frame_index + 1) % len(self.imgs)

        screen_pos = self.camera.wrld_2_scrn_coord(self.pos)

        # retrieve correct img from imgs
        self.image = self.imgs[self.frame_index]
        
        # rotating and scaling images is expensive; only do it if the sprite
        # is visible on screen; this makes the game faster at higher zooms
        if self.culling == False or \
           screen_pos.x-300 < (ssize := self.game.screen.get_size())[0] and \
           screen_pos.x+300 > 0 and \
           screen_pos.y-300 < ssize[1] and \
           screen_pos.y+300 > 0:
            # rotate and scale image 
            self.image = pg.transform.rotate(self.image, self.rot)
            self.image = pg.transform.scale(self.image, [oord*self.camera.zoom
                                            for oord in self.image.get_size()])

        # set rect position correctly
        self.rect = self.image.get_rect()
        self.rect.bottomleft = screen_pos

        # place hit_rect position correctly
        opp_corner = self.camera.wrld_2_scrn_coord(self.pos + vec2(1,-1))
        self.hit_rect = pg.rect.Rect(0,0,self.rect[2], self.rect[2])
        self.hit_rect.bottomleft = screen_pos


    def get_facing_offset(self):
        """returns the direction the sprite is facing"""
        if 45 <= self.rot % 360 < 135:
            return vec2(1,0)
        elif 135 <= self.rot % 360 < 225:
            return vec2(0,-1)
        elif 225 <= self.rot % 360 < 315:
            return vec2(-1,0)
        else:
            return vec2(0,1)


class Player(Renderable_Sprite):
    def __init__(self, game, start_pos):
        # call parent constructor
        super().__init__(game, start_pos, 0)
        self.maze = self.game.level.maze

        self.colour = 0
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

        right_imgs = [[self.game.img_loader.get(f"player_{colour}3")
                           for colour in colour_names], \
                          [self.game.img_loader.get(f"player_{colour}2")
                           for colour in colour_names]]
        right_imgs += right_imgs.copy()

        left_imgs = [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in right_imgs]

        down_imgs = [[self.game.img_loader.get(f"player_{colour}5")
                          for colour in colour_names], \
                         [self.game.img_loader.get(f"player_{colour}4")
                          for colour in colour_names]]
        down_imgs += [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in down_imgs]

        up_imgs = [[self.game.img_loader.get(f"player_{colour}1")
                          for colour in colour_names], \
                         [self.game.img_loader.get(f"player_{colour}0")
                          for colour in colour_names]]
        up_imgs += [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in up_imgs]

        self.standing_imgs = {  (1,0)  : [right_imgs[1]],
                                (-1,0) : [left_imgs[1]],
                                (0,-1) : [down_imgs[1]],
                                (0,1)  : [up_imgs[1]]
                             }
        self.walking_imgs =  {  (1,0)  : right_imgs,
                                (-1,0) : left_imgs,
                                (0,-1) : down_imgs,
                                (0,1)  : up_imgs
                             }
        # sounds
        self.walk_sounds = []
        for i in range(1,9):
            self.walk_sounds.append(self.game.snd_loader.get( \
                                    f"stepdirt_{i}.wav"))
        self.key_collect_snd = self.game.snd_loader.get("key_pickup.wav")
        self.block_collect_snd = self.game.snd_loader.get("stepstone_4.wav")
        self.block_place_snd = self.game.snd_loader.get("stepstone_1.wav")
        self.gateway_open_snd = self.game.snd_loader.get("DoorOpen07.ogg")
        self.respawn_snd = self.game.snd_loader.get("Hit_Hurt6.wav")
        self.hurt_snd = self.game.snd_loader.get("Hit_Hurt6.wav")

        self.step_sound_timer = self.game.config.player_step_snd_delay

        # set up other mechanics
        self.inventory = [False, False]
        # stores the previous key state for edge detection
        self.prev_slot_keys = [False, False]
        # stores colour keys state:
        self.colour_key_pressed = False

        self.keys = 0
        self.last_checkpoint = False

        # render once to set up rect for collisions
        self.walking = False
        self.render(0)
        
    def update(self, dt):
        # acceleration due to wasd
        keys = pg.key.get_pressed()
        walking_x = False
        walking_y = False
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            # acc left
            self.vel.x -= self.acc * dt/1000
            walking_x = True
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            # acc right
            self.vel.x += self.acc * dt/1000
            walking_x = True
     
        elif keys[pg.K_UP] or keys[pg.K_w]:
            # acc up
            self.vel.y -= self.acc * dt/1000
            walking_y = True
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            # acc down
            self.vel.y += self.acc * dt/1000
            walking_y = True

        # decelerate back to vel = 0 if not walking
        if not walking_x:
            self.vel.x -= min(self.acc * self.vel.x, self.vel.x*0.9,
                              key = lambda x: abs(x))
        if not walking_y:
            self.vel.y -= min(self.acc * self.vel.y, self.vel.y*0.9,
                              key = lambda x: abs(x))
        self.walking = walking_x or walking_y

        # enforce max speed
        self.vel = vec2([min(max(-self.max_speed, self.vel[i]), self.max_speed)\
                    for i in (0,1)])

        # block picking and placing
        slot_keys = [keys[pg.K_q], keys[pg.K_e]]
        for slot_index in (0,1):
            # only trigger on the rising edge of the key press
            if slot_keys[slot_index] and not self.prev_slot_keys[slot_index]:
                # if the slot is empty, pick up
                if self.inventory[slot_index] == False:
                    self.pick_up(slot_index)
                # if slot is full, place
                else:
                    self.place(slot_index)
        self.prev_slot_keys = slot_keys

        # get which keys are pressed for colour changing
        colour_keys = [keys[k] for k in (pg.K_1, pg.K_2, pg.K_3,
                                         pg.K_4, pg.K_5, pg.K_6)]
        # only change colour on rising edge a a key being pressed
        if not self.colour_key_pressed:
            for key_index in range(0,6):
                if colour_keys[key_index]:
                    self.colour = key_index 

        self.colour_key_pressed = max(colour_keys)

        # collisions with keys
        hits = pg.sprite.spritecollide(self,
                                       self.maze.keys,
                                       True,
                                       collide_hit_rect)
        self.keys += len(hits)
        if len(hits):
            self.key_collect_snd.play()

        # collisions with enemies
        hits = pg.sprite.spritecollide(self,
                                       self.maze.enemies,
                                       False,
                                       collide_hit_rect)
        if [h for h in hits if h.colour != self.colour]:
            # only take damage if hurt cooldown has elapsed
            if self.hurt_cooldown <= 0:
                # reset hurt cooldown
                self.hurt_cooldown = self.game.config.player_hurt_cooldown
                # take damage
                self.health -= 1
                # play hurt sound
                self.hurt_snd.play()

        # decrease hurt cooldown
        self.hurt_cooldown = max(0, self.hurt_cooldown - dt)

        # play step sound if step sound timer has elapsed
        if self.walking:
            if self.step_sound_timer <= 0:
                rng.choice(self.walk_sounds).play()
                self.step_sound_timer = self.game.config.player_step_snd_delay
            else:
                self.step_sound_timer -= dt
        else:
            self.step_sound_timer = 0

        # update rot based on movement
        if self.vel.length != 0:
            self.rot = self.vel.angle_to(vec2(0,1))

        # collide with walls
        self.collide()

        # change position by velocity
        self.pos += self.vel

        # respawn
        if self.health == 0:
            self.respawn()

        # change layer
        self.maze.all_sprites.change_layer(self, int(self.pos.y))

    def pick_up(self, slot_index):
        """picks up block in front of the player and stores in inventory"""
        # slot is already full
        if self.inventory[slot_index]:
            return

        # find block in front of the player
        facing_pos = (self.pos+vec2(0.25,0.75))//1 + self.get_facing_offset()
        facing_sprite = self.maze.board[int(facing_pos.y)][int(facing_pos.x)]

        # check if it is a block
        if type(facing_sprite).__name__ == "Block":
            # store this block to inventory
            self.inventory[slot_index] = facing_sprite

            # remove this block from board
            self.maze.board[int(facing_pos.y)][int(facing_pos.x)] = False

            # remove block from all sprites and blocks
            self.maze.blocks.remove(facing_sprite)
            self.maze.all_sprites.remove(facing_sprite)

            # play block collection sound
            self.block_collect_snd.play()
    
    def place(self, slot_index):
        """places a block in front of the player from inventory slot"""
        # nothing to place
        if self.inventory[slot_index] == False:
            return
            
        # find block in front of the player
        facing_pos = (self.pos+vec2(0.25,0.75))//1 + self.get_facing_offset()
        facing_sprite = self.maze.board[int(facing_pos.y)][int(facing_pos.x)]
        
        # ensure the space is free before placing in a free space
        if facing_sprite == False:
            # remove block from inventory
            block = self.inventory[slot_index]
            self.inventory[slot_index] = False
            
            # set block's new position
            block.pos = facing_pos//1

            # store block in inventory there
            self.maze.board[int(facing_pos.y)][int(facing_pos.x)] = block

            # add block to all sprites and blocks
            self.maze.all_sprites.add(block)
            self.maze.blocks.add(block)

            # change block's layer so it renders correctly
            self.maze.all_sprites.change_layer(block, int(block.pos.y))

            # play placing sound
            self.block_place_snd.play()

        # if space isn't free, check if it is a gateway
        if type(facing_sprite).__name__ == "Gateway" and \
                facing_sprite.colour == self.inventory[slot_index].colour:
            # remove both the block and gateway
            self.inventory[slot_index].kill()
            self.inventory[slot_index] = False

            facing_sprite.kill()
            self.maze.board[int(facing_pos.y)][int(facing_pos.x)] = False
            self.gateway_open_snd.play()

    def respawn(self):
        """respawns the player at the correct location when they die"""
        # play respawn sound
        self.respawn_snd.play()

        # set health to player max health
        self.health = self.game.config.player_max_health

        if self.last_checkpoint != False:
            self.pos = vec2(self.last_checkpoint.pos)
        else:
            self.pos = vec2(self.maze.start)

    def collide(self):
        # overcomplicated collisions to remove wierd snapping
        # - no dependency on velocities, which can cause problems

        def check_collidable(sprite):
             return type(sprite).__name__ == "Wall" or \
                    (type(sprite).__name__ == "Block" and 
                    sprite.colour != self.colour) or \
                    type(sprite).__name__ == "Gateway" or \
                    type(sprite).__name__ == "Exit" and self.keys != 6

        board = self.maze.board

        for sprite in self.maze.all_sprites:
            if collide_hit_rect(sprite, self) and check_collidable(sprite):

                if self.hit_rect.x+10 > sprite.hit_rect.right:
                    # wall on left
                    spot = sprite.pos//1 + vec2(1,0)

                    # collide if outside the bounds or isnt a collideable
                    if not(0 <= spot.x < self.maze.bsize[0]) or \
                       not(check_collidable(board[int(spot.y)][int(spot.x)])):
                        self.vel.x = max(0, self.vel.x)

                elif self.hit_rect.bottom-10 < sprite.hit_rect.y:
                    # wall below
                    spot = sprite.pos//1 + vec2(0,-1)
                    
                    # collide if outside the bounds or isnt a collideable
                    if not(0 <= spot.y < self.maze.bsize[0]) or \
                       not(check_collidable(board[int(spot.y)][int(spot.x)])):
                        self.vel.y = min(0, self.vel.y)

                elif self.hit_rect.right-10 < sprite.hit_rect.x:
                    # wall on right
                    spot = sprite.pos//1 + vec2(-1,0)
                    
                    # collide if outside the bounds or isnt a collideable
                    if not(0 <= spot.x < self.maze.bsize[0]) or \
                       not(check_collidable(board[int(spot.y)][int(spot.x)])):
                        self.vel.x = min(0, self.vel.x)

                elif self.hit_rect.y+10 > sprite.hit_rect.bottom:
                    # wall above
                    spot = sprite.pos//1 + vec2(0,1)
                    
                    # collide if outside the bounds or isnt a collideable
                    if not(0 <= spot.y < self.maze.bsize[0]) or \
                       not(check_collidable(board[int(spot.y)][int(spot.x)])):
                        self.vel.y = max(0, self.vel.y)

    def render(self, dt):
        """render the player sprite"""
        facing_dir = self.get_facing_offset()

        # retrieve correct set of imgs for player's current rotation
        if self.walking:
            self.imgs = self.walking_imgs[tuple(facing_dir)]
        else:
            self.imgs = self.standing_imgs[tuple(facing_dir)]
            self.frame_index = 0
        
        # decrease frame_countdown 
        self.frame_countdown -= dt
        # advance to next frame if less than 0
        if self.frame_countdown < 0:
            self.frame_countdown = self.frame_time
            self.frame_index = (self.frame_index + 1) % len(self.imgs) 

        # retrieve correct img from imgs
        self.image = self.imgs[self.frame_index][self.colour]
        self.image = pg.transform.scale(self.image, 
                                  [oord * self.camera.zoom // 2 for
                                   oord in self.image.get_size()])

        # data for rendering of blocks in inventory
        b1_pos = {(0,-1) : vec2(3,6),
                  (1,0)  : vec2(0,6),
                  (-1,0) : vec2(6,6)}
        b2_pos = {(0,-1) : vec2(3,4.5),
                  (1,0)  : vec2(0,4.5),
                  (-1,0) : vec2(6,4.5)}

        # render blocks in inventory so that they scale correctly
        for block in self.inventory:
            if block:
                block.render(0)

        # no image if facing down
        if facing_dir != (0,1):
            # work out the position and size of each block's image
            if block_1 := self.inventory[0]:
                block_1_image = pg.transform.scale(
                    block_1.image, vec2(block_1.image.get_size())//8)

                block_1_pos = b1_pos[tuple(facing_dir)] * self.camera.zoom

            if block_2 := self.inventory[1]:
                block_2_image = pg.transform.scale(
                    block_2.image, vec2(block_2.image.get_size())//8)

                block_2_pos = b2_pos[tuple(facing_dir)] * self.camera.zoom

            # blit on top if facing up, otherwise blit behind
            if facing_dir == (0,-1):
                if block_1:
                    self.image.blit(block_1_image, block_1_pos)
                if block_2:
                    self.image.blit(block_2_image, block_2_pos)
            else:
                image = pg.surface.Surface(self.image.get_size(),
                                           flags = pg.SRCALPHA)
                if block_1:
                    image.blit(block_1_image,block_1_pos)
                if block_2:
                    image.blit(block_2_image, block_2_pos)
                image.blit(self.image, (0,0))
                self.image = image

        # set rect position correctly
        self.rect = self.image.get_rect()
        screen_pos = self.camera.wrld_2_scrn_coord(self.pos)
        self.rect.bottomleft = screen_pos

        # place hit_rect position correctly
        opp_corner = self.camera.wrld_2_scrn_coord(self.pos + vec2(1,-1))
        self.hit_rect = pg.rect.Rect(0,0,self.rect[2], self.rect[2])
        self.hit_rect.bottomleft = screen_pos


class Enemy(Renderable_Sprite):
    def __init__(self, game, start_pos):
        super().__init__(game, start_pos)
        self.colour = rng.randint(0,5)
        self.maze = self.game.level.maze

        # load all animation frames from img loader

        left_imgs = [[self.game.img_loader.get(f"enemy_{colour}{i}")
                           for colour in colour_names]
                           for i in range(4)]
                          
        right_imgs = [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in left_imgs]

        up_imgs = [[self.game.img_loader.get(f"enemy_{colour}6")
                          for colour in colour_names], \
                         [self.game.img_loader.get(f"enemy_{colour}7")
                          for colour in colour_names]]
        up_imgs += [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in up_imgs]
        
        down_imgs = [[self.game.img_loader.get(f"enemy_{colour}4")
                          for colour in colour_names], \
                         [self.game.img_loader.get(f"enemy_{colour}5")
                          for colour in colour_names]]
        down_imgs += [[pg.transform.flip(img, True, False)
                          for img in frame]
                          for frame in down_imgs]

        self.walking_imgs = {   (-1,0)  : left_imgs,
                                (1,0) : right_imgs,
                                (0,1)  : down_imgs,
                                (0,-1) : up_imgs
                    }
        
        # get a path
        self.get_path()


    def get_path(self):
        """calculates a new path for this sprite to follow"""

        current_pos = (self.pos+vec2(0.25,0.75))//1
        current_pos = (int(current_pos.x), int(current_pos.y))
        destination = self.maze.branch(current_pos, [])

        # find path to this location
        self.target_path = self.maze.get_shortest_path(current_pos, destination)

    def update(self, dt):
        # get direction to current target
        target = vec2(self.target_path[0]) + vec2(0.25, -0.25)
        target_delta = target - self.pos

        # if it has reached the target, remove it from target_path
        if target_delta.length() < 0.05:
            self.target_path.pop(0)
            
            # if the whole path has been followed, generate a new one
            if len(self.target_path) == 0:
                self.get_path()

            # recompute target
            target = vec2(self.target_path[0])
            target_delta = target - self.pos

        # move towards target
        if target_delta.length() != 0:
            self.vel = target_delta.normalize() * self.game.config.enemy_speed
            self.rot = self.vel.angle_to(vec2(0,1))
            self.pos += self.vel

        # change layer
        self.maze.all_sprites.change_layer(self, int(self.pos.y))

    def render(self, dt):
        """render the enemy sprite"""
        facing_dir = self.get_facing_offset()
        self.imgs = self.walking_imgs[tuple(facing_dir)]
        
        # decrease frame_countdown 
        self.frame_countdown -= dt
        # advance to next frame if less than 0
        if self.frame_countdown < 0:
            self.frame_countdown = self.frame_time
            self.frame_index = (self.frame_index + 1) % len(self.imgs) 

        # retrieve correct img from imgs
        self.image = self.imgs[self.frame_index][self.colour]
        self.image = pg.transform.scale(self.image, 
                                  [oord * self.camera.zoom // 1.5 for
                                   oord in self.image.get_size()])
        
        # set rect position correctly
        self.rect = self.image.get_rect()
        screen_pos = self.camera.wrld_2_scrn_coord(self.pos)
        self.rect.bottomleft = screen_pos

        # place hit_rect position correctly
        opp_corner = self.camera.wrld_2_scrn_coord(self.pos + vec2(1,-1))
        self.hit_rect = pg.rect.Rect(0,0,self.rect[2], self.rect[2])
        self.hit_rect.bottomleft = screen_pos


class Wall(Renderable_Sprite):
    def __init__(self, game, start_pos):
        super().__init__(game, start_pos)

        # initialise assets
        self.imgs = [game.img_loader.get("brick dark grey")]


class Gateway(Renderable_Sprite):
    def __init__(self, game, start_pos, colour):
        super().__init__(game, start_pos)
        self.colour = colour

        # initialise assets
        self.imgs = [game.img_loader.get(
                                    f"gateway_{colour_names[self.colour]}")]


class Block(Renderable_Sprite):
    def __init__(self, game, start_pos, colour):
        super().__init__(game, start_pos)
        self.colour = colour
        self.culling = False

        # initialise assets
        match self.colour:
            case 0:
                self.imgs = [game.img_loader.get(f"crate light red")]
            case 1:
                self.imgs = [game.img_loader.get(f"crate orange")]
            case 2:
                self.imgs = [game.img_loader.get(f"crate lime")]
            case 3:
                self.imgs = [game.img_loader.get(f"crate dark blue")]
            case 4:
                self.imgs = [game.img_loader.get(f"crate purple")]
            case 5:
                self.imgs = [game.img_loader.get(f"crate light blue")]


class Checkpoint(Renderable_Sprite):
    def __init__(self, game, start_pos):
        super().__init__(game, start_pos)

        self.active = False

        # init active images
        self.active_imgs = []
        for img_index in range(0,6):
            img = self.game.img_loader.get(f"Flag{img_index}")
            self.active_imgs.append(img)
        # init deactive images
        self.deactive_imgs = []
        for img_index in range(0,2):
            img = self.game.img_loader.get(f"Flag_down{img_index}")
            self.deactive_imgs.append(img)
        # innit
        self.imgs = self.deactive_imgs

    def update(self, dt):
        if not self.active:
            if (self.pos - self.game.level.player.pos).length() < 0.5:
                # deactivate currently active checkpoint
                if last_checkpoint := self.game.level.player.last_checkpoint:
                    last_checkpoint.deactivate()

                # activate this checkpoint
                self.activate()

    def activate(self):
        """activates this checkpoint"""
        self.active = True
        self.imgs = self.active_imgs
        self.game.level.player.last_checkpoint = self

    def deactivate(self):
        """deactivates this checkpoint"""
        self.active = False
        self.imgs = self.deactive_imgs
        self.frame_index = 0
 

class Key(Renderable_Sprite):
    def __init__(self, game, start_pos):
        super().__init__(game, start_pos)

        key_frame_count = self.game.config.key_frame_count
        key_displacement = self.game.config.key_displacement

        # generate images
        key_image = self.game.img_loader.get("key cream")
        key_image = pg.transform.scale(key_image, vec2(key_image.get_size()))
        self.imgs = []

        for i in range(key_frame_count):
            displaced_img = pg.surface.Surface(
                key_image.get_size() + vec2(0,key_displacement),
                flags = pg.SRCALPHA)

            # calculate how far this image must be moved
            offset = (math.cos(2*math.pi * (i/key_frame_count) ) + 1) \
                     * key_displacement // 2

            # blit key image to displaced image in correct location
            displaced_img.blit(key_image, (0, offset))

            # append to imgs
            self.imgs.append(displaced_img)


class Exit(Renderable_Sprite):
    def __init__(self, game, start_pos):
        super().__init__(game, start_pos)

        # load images
        self.state_imgs = []
        for img_index in range(0,7):
            self.state_imgs.append(
                            self.game.img_loader.get(f"exit_locked{img_index}"))
        self.state_imgs.append(self.game.img_loader.get("exit_open"))
        self.imgs = [self.state_imgs[0]]
        self.opened = False

    def update(self, dt):
        keys = self.game.level.player.keys
        player_pos = (self.game.level.player.pos+vec2(0.25,0.75))//1 
        
        if self.opened:
            self.imgs = [self.state_imgs[-1]]
            self.frame_index = 0
        else:
            if (player_pos - self.pos).length() < 2:
                self.imgs = self.state_imgs[-2:] * 6
                if self.frame_index == len(self.imgs)-1:
                    self.opened = True
            else:
                self.imgs = [self.state_imgs[keys]]
        


class Camera():
    def __init__(self, game, target = False):
        self.game = game
        self.target = target
        self.pos = vec2(0,0) # this location is the centre of the screen
        self.zoom = self.game.config.camera_zoom

        # invisible default image to support being part of all sprites
        self.img = pg.surface.Surface((1,1))
        self.img.fill((0,0,0))
        self.rect = self.img.get_rect()
        self.rect.topleft = (-1000,-1000)

    def set_target(self, target):
        """sets the sprite which the camera should follow"""
        self.target = target
    
    def update(self, dt):
        """updates the position of the camera so that it tracks the player"""

        # adjust the camera pos
        target_pos = vec2(self.target.pos)
        target_pos_delta = -(target_pos - self.pos)
        self.pos = self.pos - 0.1*target_pos_delta 

        # ensure camera never goes of screen
        unscaled_scrn_size = vec2(self.game.config.resolution)/ self.zoom / 16
        wrld_size = vec2(self.game.level.maze.bsize)

        left_edge = unscaled_scrn_size.x/2
        right_edge = wrld_size.x - unscaled_scrn_size.x/2
        top_edge = unscaled_scrn_size.y/2 - 1.4
        bottom_edge = wrld_size.y - unscaled_scrn_size.y/2 - 1.3

        self.pos.x = min(max(left_edge, self.pos.x), right_edge)
        self.pos.y = min(max(top_edge, self.pos.y), bottom_edge)

    def wrld_2_scrn_coord(self, wrld_coord):
        """takes a world space coordinate and converts it to screenspace"""
        scrn_size = vec2(self.game.config.resolution)

        # ensures that the cameras position ends up at the centre of the screen
        scaled_wrld_coord = vec2(wrld_coord) * self.zoom * 16
        scaled_pos = self.pos * self.zoom * 16
        ss_coord = scaled_wrld_coord + scrn_size/2 - scaled_pos
        return ss_coord


class Timer():
    def __init__(self, game):
        self.game = game
        self.reset()

        # invisible default image to support being part of all sprites
        self.img = pg.surface.Surface((1,1))
        self.img.fill((0,0,0))
        self.rect = self.img.get_rect()
        self.rect.topleft = (-1000,-1000)

    def update(self, dt):
        # dt is in ms, but total time is in s so dt is scalled correctly
        self.total_time += dt/1000

    def reset(self):
        self.total_time = 0.0
        self.start_time = time.time()