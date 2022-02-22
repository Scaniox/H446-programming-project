import pygame as pg
import config as cfg
import Asset_Loader as AL
import Menu_Sprites as MS

vec2 = pg.math.Vector2


class Game():
    def __init__(self):
        # init pygame
        pg.init()
        pg.key.set_repeat(500, 50)
        
        # config
        self.config = cfg.Config()
        
        # init screen
        self.screen = pg.display.set_mode(self.config.resolution,
                                          flags = pg.RESIZABLE)

        # init asset loaders
        self.img_loader = AL.Img_Loader(self)
        self.snd_loader = AL.Snd_Loader(self)

        # run level level
        self.level = Level(self)

        clock = pg.time.Clock()
        while True:
            dt = clock.tick(75)
            events = list(pg.event.get())
            for event in events:
                if event.type == pg.QUIT:
                    return
                if event.type == pg.VIDEORESIZE:
                    self.level.rescale()

            self.level.tick(dt, events)

            pg.display.flip()

class Level():
    def __init__(self, game):
        self.game = game
        self.sprites = pg.sprite.Group()

        self.text = MS.Text(self.game, pg.rect.Rect(0,0,300,50), "text 1")
        self.sprites.add(self.text)

        self.input_box = MS.Input_Box(self.game, 
                                 pg.rect.Rect(0,0,300,50),
                                 "input box 1", 
                                 MS.k2c_all)
        self.sprites.add(self.input_box)

        self.toggle = MS.Toggle(self.game, pg.rect.Rect(0,0,50,50))
        self.sprites.add(self.toggle)

        self.slider = MS.Slider(self.game, pg.rect.Rect(0,0,400,40))
        self.sprites.add(self.slider)

        self.spinner = MS.Spinner(self.game, pg.rect.Rect(0,0,350,50),
                                  ["option 1","option 2","option 3"])
        self.sprites.add(self.spinner)
        
        self.button = MS.Button(self.game, pg.rect.Rect(0,0,300,50), "button 1")
        self.sprites.add(self.button)

        self.rescale()


    def tick(self, dt, events):
        for sprite in self.sprites:
            sprite.update(dt, events)

        self.game.screen.fill((0,0,0))
        self.sprites.draw(self.game.screen)

    def rescale(self):
        screen_size = vec2(pg.display.get_window_size())
        # reposition all the sprites
        
        self.text.rect.center = (screen_size.x * 1/6, screen_size.y * 1/4)
        self.input_box.rect.center = (screen_size.x * 3/6, screen_size.y * 1/4)
        self.toggle.rect.center = (screen_size.x * 5/6, screen_size.y * 1/4)
        
        self.slider.rect.center = (screen_size.x * 1/6, screen_size.y * 3/4)
        self.spinner.rect.center = (screen_size.x * 3/6, screen_size.y * 3/4)
        self.button.rect.center = (screen_size.x * 5/6, screen_size.y * 3/4)

        for sprite in self.sprites:
            sprite.rescale()
        
Game()
