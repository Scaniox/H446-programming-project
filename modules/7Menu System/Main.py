import pygame as pg
import config as cfg
import Asset_Loader as AL
import Menu_System as MSYS

class Game():
    def __init__(self):
        self.game_state_stack = []

        # init pygame env
        pg.init()
        pg.mixer.init()

        # init config
        self.config = cfg.Config()

        # init video
        self.set_screen()

        # init loaders
        self.img_loader = AL.Img_Loader(self)
        self.snd_loader = AL.Snd_Loader(self)

        # init screens other than level
        self.main_screen = MSYS.Main(self)
        self.pause_screen = MSYS.Pause(self)
        self.options_screen = MSYS.Options(self)
        self.gfx_options_screen = MSYS.GFX_Options(self)
        self.snd_options_screen = MSYS.SND_Options(self)
        self.scoreboard_screen = MSYS.Scoreboard(self)
        self.start_screen = MSYS.Start(self)
        self.end_screen = False
        self.level = False

        # load and play background music
        self.music = self.snd_loader.get("Vexento - Lotus.mp3")
        self.load_snd_vol()
        self.music.play(loops = -1)

        # push main menu onto game state stack
        self.game_state_stack.append(self.main_screen.tick)

        # call run
        self.run()

        # after running terminates, close
        pg.quit()

    def run(self):
        # main loop
        clock = pg.time.Clock()
        while len(self.game_state_stack) > 0:
            # calculate dt
            if self.config.vsync:
                # delay to achieve correct frame rate
                dt = clock.tick(60)
            else:
                dt = clock.tick()

            # event collect events
            event_list = list(pg.event.get())

            # check events
            for event in event_list:
                # close event: close the game
                if event.type == pg.QUIT:
                    return
                
                # rescale events: change size of the screen
                elif event.type == pg.VIDEORESIZE:
                    if self.config.rescaleable:
                        self.config.resolution = event.size
                        self.rescale()

            # call correct tick function
            self.game_state_stack[-1](event_list, dt)

            pg.display.flip()

    def start_level(self, size, seed):
        # validate
        if size[0] <= 0 or size[1] <= 0:
            print(f"invalid level size: {size}")
            return

        # initialise new level
        self.level = MSYS.Level(self, size, seed)

        # push tick function to game state stack
        self.game_state_stack.append(self.level.tick)

    def load_snd_vol(self):
        # change music volume
        self.music.set_volume(self.config.music_vol)

    def set_screen(self):
        """sets the display mode based on parameters in config"""
        # fullscreen
        if self.config.fullscreen:
            desired_res = pg.display.get_desktop_sizes()[0]
            self.screen = pg.display.set_mode(desired_res, flags=pg.FULLSCREEN)            

        # rescale screen
        elif self.config.rescaleable:
            self.screen = pg.display.set_mode(self.config.resolution,
                                              pg.RESIZABLE)
        else:
            self.screen = pg.display.set_mode(self.config.resolution)

    def rescale(self):
        self.set_screen()

        # call rescale method of all screens
        self.main_screen.rescale()
        self.pause_screen.rescale()
        self.options_screen.rescale()
        self.gfx_options_screen.rescale()
        self.snd_options_screen.rescale()
        self.scoreboard_screen.rescale()
        self.start_screen.rescale()
        if self.end_screen:
            self.end_screen.rescale()
        if self.level:
            self.level.rescale()

Game()