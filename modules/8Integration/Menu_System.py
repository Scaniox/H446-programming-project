import pygame as pg
import Menu_Sprites as MS
import Sprites as sprites
import Maze_Gen as mg
import random as rng

vec2 = pg.math.Vector2
default_rect = lambda : pg.rect.Rect(0,0,1,1)

class Ui_Screen():
    def __init__(self, game):
        self.game = game

        self.elements = pg.sprite.Group()
        self.background = False

        self.screen = self.game.screen

    def tick(self, event_list, dt):
        self.elements.update(dt, event_list)
        if self.background:
            self.game.screen.blit(self.bg_img, self.bg_rect)
        self.elements.draw(self.game.screen)

    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # rescale the background if it is present
        if self.background:
            # choose scale factor to fill screen
            match_width_SF = screen_rect.width / self.background.get_width()
            match_height_SF = screen_rect.height / self.background.get_height()
            scale_factor = max(match_height_SF, match_width_SF)
            
            # rescale image
            background_size = vec2(self.background.get_size()) * scale_factor
            self.bg_img = pg.transform.scale(self.background, background_size)
            
            # position image
            self.bg_rect = self.bg_img.get_rect()
            self.bg_rect.center = screen_rect.center

        # rescale all elements
        for elements in self.elements:
            elements.rescale()

class Main(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.title_text = MS.Text(game, default_rect(),
                                  "Colour Between The Lines")
        self.elements.add(self.title_text)
        self.start_b = MS.Button(game, default_rect(), "Start")
        self.elements.add(self.start_b)
        self.options_b = MS.Button(game, default_rect(), "Options")
        self.elements.add(self.options_b)
        self.scoreboard_b = MS.Button(game, default_rect(), "Scoreboard")
        self.elements.add(self.scoreboard_b)
        self.close_b = MS.Button(game, default_rect(), "Close")
        self.elements.add(self.close_b)
        # load background image
        self.background = game.img_loader.get("main background")

        # call rescale to render image
        self.rescale()

    def tick(self, event_list, dt):
        # call parent tick function
        super().tick(event_list, dt)
        # push tick functions onto GSS for button presses

        # start
        if self.start_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.start_screen.tick)
        # options
        elif self.options_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.options_screen.tick)
        # scoreboard
        elif self.scoreboard_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.scoreboard_screen.tick)
        # close
        elif self.close_b.falling_edges[0]:
            self.game.game_state_stack = []
    
    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.title_text.rect.width = screen_size.x 
        self.title_text.rect.height = screen_size.y / 10
        self.title_text.rect.centerx = screen_rect.centerx
        self.title_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y * 2 / 6

        # start button
        self.start_b.rect.width = button_width
        self.start_b.rect.height = button_height
        self.start_b.rect.centerx = screen_rect.centerx
        self.start_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # options button
        self.options_b.rect.width = button_width
        self.options_b.rect.height = button_height
        self.options_b.rect.centerx = screen_rect.centerx
        self.options_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # scoreboard button
        self.scoreboard_b.rect.width = button_width
        self.scoreboard_b.rect.height = button_height
        self.scoreboard_b.rect.centerx = screen_rect.centerx
        self.scoreboard_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # close button
        self.close_b.rect.width = button_width
        self.close_b.rect.height = button_height
        self.close_b.rect.centerx = screen_rect.centerx
        self.close_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale()


class Pause(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.pause_text = MS.Text(game, default_rect(), "Pause")
        self.elements.add(self.pause_text)
        self.resume_b = MS.Button(game, default_rect(), "Resume")
        self.elements.add(self.resume_b)
        self.options_b = MS.Button(game, default_rect(), "Options")
        self.elements.add(self.options_b)
        self.exit_b = MS.Button(game, default_rect(), "Main Menu")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()

    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # resume button
        if self.resume_b.falling_edges[0]:
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack.pop(-1)
                break

        # options button
        if self.options_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.options_screen.tick)

        # exit button
        elif self.exit_b.falling_edges[0]:
            self.game.game_state_stack = [self.game.main_screen.tick]
    
    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.pause_text.rect.width = screen_size.x
        self.pause_text.rect.height = screen_size.y / 10
        self.pause_text.rect.centerx = screen_rect.centerx
        self.pause_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y / 4

        # resume button
        self.resume_b.rect.width = button_width
        self.resume_b.rect.height = button_height
        self.resume_b.rect.centerx = screen_rect.centerx
        self.resume_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # options button
        self.options_b.rect.width = button_width
        self.options_b.rect.height = button_height
        self.options_b.rect.centerx = screen_rect.centerx
        self.options_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = button_width
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale()

class Options(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.options_text = MS.Text(game, default_rect(), "Options")
        self.elements.add(self.options_text)
        self.gfx_b = MS.Button(game, default_rect(), "Graphics")
        self.elements.add(self.gfx_b)
        self.snd_b = MS.Button(game, default_rect(), "Sound")
        self.elements.add(self.snd_b)
        self.exit_b = MS.Button(game, default_rect(), "Exit")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()

    def tick(self, events, dt):
        # call parent tick function
        super().tick(events, dt)

        # gfx button
        if self.gfx_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.gfx_options_screen.tick)
        
        # snd button
        if self.snd_b.falling_edges[0]:
            self.game.game_state_stack.append(self.game.snd_options_screen.tick)

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack.pop(-1)
                break

    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.options_text.rect.width = screen_size.x
        self.options_text.rect.height = screen_size.y / 10
        self.options_text.rect.centerx = screen_rect.centerx
        self.options_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y / 4

        # gfx button
        self.gfx_b.rect.width = button_width
        self.gfx_b.rect.height = button_height
        self.gfx_b.rect.centerx = screen_rect.centerx
        self.gfx_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # snd button
        self.snd_b.rect.width = button_width
        self.snd_b.rect.height = button_height
        self.snd_b.rect.centerx = screen_rect.centerx
        self.snd_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = button_width
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale()

    
class GFX_Options(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.gfx_text = MS.Text(game, default_rect(), "Graphics")
        self.elements.add(self.gfx_text)
        self.res_sp = MS.Spinner(game, default_rect(), ["640x480",
                                                        "800x600",
                                                        "1280x720",
                                                        "1366x768",
                                                        "1600x900",
                                                        "1920x1080",
                                                        "Rescalable"])
        self.elements.add(self.res_sp)
        if game.config.rescaleable:
            res_n = "Rescalable"
        else:
            res_n = f"{game.config.resolution[0]}x{game.config.resolution[1]}"
        self.res_sp.index = self.res_sp.options.index(res_n)

        self.fullscreen_text = MS.Text(game, default_rect(), "Fullscreen")
        self.elements.add(self.fullscreen_text)
        self.Vsync_text = MS.Text(game, default_rect(), "Vsync") 
        self.elements.add(self.Vsync_text)

        self.fullscreen_tg = MS.Toggle(game, default_rect())
        self.elements.add(self.fullscreen_tg)
        self.fullscreen_tg.ticked = game.config.fullscreen

        self.Vsync_tg = MS.Toggle(game, default_rect())
        self.elements.add(self.Vsync_tg)
        self.Vsync_tg.ticked = game.config.vsync

        self.apply_b = MS.Button(game, default_rect(), "Apply")
        self.elements.add(self.apply_b)
        self.exit_b = MS.Button(game, default_rect(), "Exit")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()

    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # change settings if apply pressed
        if self.apply_b.falling_edges[0]:
            # resolution
            res_option = self.res_sp.options[self.res_sp.index]
            if res_option == "Rescalable":
                self.game.config.rescaleable = True
            else:
                self.game.config.rescaleable = False
                self.game.config.resolution = [int(i) for i in 
                                               res_option.split("x")]

            # fullscreen
            self.game.config.fullscreen = self.fullscreen_tg.ticked

            # vsync
            self.game.config.vsync = self.Vsync_tg.ticked

            # save changes
            self.game.config.save()

            self.game.rescale()

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack.pop(-1)
                break

    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.gfx_text.rect.width = screen_size.x
        self.gfx_text.rect.height = screen_size.y / 10
        self.gfx_text.rect.centerx = screen_rect.centerx
        self.gfx_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y / 4

        # res spinner
        self.res_sp.rect.width = button_width * 5/4
        self.res_sp.rect.height = button_height
        self.res_sp.rect.centerx = screen_rect.centerx
        self.res_sp.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # fullscreen text
        self.fullscreen_text.rect.width = button_width
        self.fullscreen_text.rect.height = button_height
        self.fullscreen_text.rect.centerx = screen_rect.centerx-button_width*1/6
        self.fullscreen_text.rect.centery = button_pos_y
        
        # fullscreen toggle
        self.fullscreen_tg.rect.width = button_height * 2/3
        self.fullscreen_tg.rect.height = button_height * 2/3
        self.fullscreen_tg.rect.centerx = screen_rect.centerx+button_width*1/2
        self.fullscreen_tg.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # Vsync text
        self.Vsync_text.rect.width = button_width 
        self.Vsync_text.rect.height = button_height
        self.Vsync_text.rect.centerx = screen_rect.centerx-button_width*1/6
        self.Vsync_text.rect.centery = button_pos_y
        
        # Vsync toggle
        self.Vsync_tg.rect.width = button_height * 2/3
        self.Vsync_tg.rect.height = button_height * 2/3
        self.Vsync_tg.rect.centerx = screen_rect.centerx+button_width*1/2
        self.Vsync_tg.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # apply button
        self.apply_b.rect.width = button_width
        self.apply_b.rect.height = button_height
        self.apply_b.rect.centerx = screen_rect.centerx
        self.apply_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = button_width
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale()    

class SND_Options(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.snd_text = MS.Text(game, default_rect(), "Sound")
        self.elements.add(self.snd_text)
        self.game_text = MS.Text(game, default_rect(), "Game Volume:")
        self.elements.add(self.game_text)
        self.music_text = MS.Text(game, default_rect(), "Music Volume:")
        self.elements.add(self.music_text)

        self.game_slider = MS.Slider(game, default_rect())
        self.elements.add(self.game_slider)
        self.game_slider.val = game.config.game_vol

        self.music_slider = MS.Slider(game, default_rect())
        self.elements.add(self.music_slider)
        self.music_slider.val = game.config.music_vol

        self.exit_b = MS.Button(game, default_rect(), "Exit")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()
    
    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # store sound vols to config
        self.game.config.game_vol = self.game_slider.val
        self.game.config.music_vol = self.music_slider.val

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.config.save()
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.config.save()
                self.game.game_state_stack.pop(-1)
                break

        # call game's load sound function
        self.game.load_snd_vol()

    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.snd_text.rect.width = screen_size.x
        self.snd_text.rect.height = screen_size.y / 10
        self.snd_text.rect.centerx = screen_rect.centerx
        self.snd_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y / 4

        # game volume text
        self.game_text.rect.width = button_width 
        self.game_text.rect.height = button_height * 3/4
        self.game_text.rect.centerx = screen_rect.centerx
        self.game_text.rect.centery = button_pos_y
        button_pos_y += button_spacing
        
        # game volume slider
        self.game_slider.rect.width = button_width 
        self.game_slider.rect.height = button_height / 2
        self.game_slider.rect.centerx = screen_rect.centerx
        self.game_slider.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # music volume text
        self.music_text.rect.width = button_width
        self.music_text.rect.height = button_height * 3/4
        self.music_text.rect.centerx = screen_rect.centerx
        self.music_text.rect.centery = button_pos_y
        button_pos_y += button_spacing
        
        # music volume slider
        self.music_slider.rect.width = button_width
        self.music_slider.rect.height = button_height / 2
        self.music_slider.rect.centerx = screen_rect.centerx
        self.music_slider.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = button_width
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale() 
        

class Scoreboard(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.sb_text = MS.Text(game, default_rect(), "Scoreboard")
        self.elements.add(self.sb_text)
        self.exit_b = MS.Button(game, default_rect(), "Exit")
        self.elements.add(self.exit_b)

        # score boxes
        self.score_boxes = []
        for _ in range(13):
            box = MS.Text(game, default_rect(), "") 
            self.score_boxes.append(box)
            self.elements.add(box)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.load()
        self.rescale()

    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack.pop(-1)
                break


    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.sb_text.rect.width = screen_size.x
        self.sb_text.rect.height = screen_size.y / 10
        self.sb_text.rect.centerx = screen_rect.centerx
        self.sb_text.rect.centery = screen_size.y / 16

        # render top 10 scores
        table_width = screen_size.x 
        table_row_height = screen_size.y * 1/6
        table_entry_height = screen_size.y * 1/20

        # table heading
        box = self.score_boxes[0]
        box.rect.width = table_width
        box.rect.height = table_entry_height
        box.rect.centerx = screen_rect.centerx
        box.rect.centery = table_row_height
        table_row_height += table_entry_height
        box.text = \
        f"# |{'Name':^15}|{'time':^6}|{'width':^6}|{'height':^6}|{'seed':^8}"

        # sort by shortest time
        sorted_scores = sorted(self.scoreboard_data, key = lambda x : int(x[1]))

        # set data for each box
        for i in range(1,13):
            # set row position
            box = self.score_boxes[i]
            box.rect.width = table_width
            box.rect.height = table_entry_height
            box.rect.centerx = screen_rect.centerx
            box.rect.centery = table_row_height
            table_row_height += table_entry_height

            # set row text
            if len(sorted_scores) > i-1:
                r = sorted_scores[i-1]
                box.text = \
                f"{i:^2}|{r[0]:^15}|{r[1]:^6}|{r[2]:^6}|{r[3]:^6}|{r[4]:^8}"
            else:
                box.text = f"{i:^2}|{'':^15}|{'':^6}|{'':^6}|{'':^6}|{'':^8}"

        # exit button
        self.exit_b.rect.width = screen_size.x / 3
        self.exit_b.rect.height = screen_size.y / 14
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = screen_size.y * 7/8

        # call parent rescale method
        super().rescale()

    def load(self):

        try:
            # load scoreboard file
            scores_file = open(self.game.config.scoreboard_pathX, "r")
            
            # split by lines
            self.scoreboard_data = []
            for line in scores_file.readlines():
                self.scoreboard_data.append(line.strip().split(","))

            # close scoreboard file
            scores_file.close()
        except:
            print(f"failed to read scoreboard file")
            self.scoreboard_data = []

    def save(self):
        # convert data to a string
        output_str = ""
        for row in self.scoreboard_data:
            for column in row:
                output_str += f"{column},"
            output_str = output_str[:-1]
            output_str += "\n"

        try:
            # load scoreboard file
            scores_file = open(self.game.config.scoreboard_pathX, "w")

            # write to file
            scores_file.write(output_str)

            # close file
            scores_file.close()
        except Exception as error:
            print(f"failed to write scoreboard file: {error}")

    def add_score(self, name, time, width, height, seed):
        # load data before appending to it
        self.load()

        # add new data
        self.scoreboard_data.append([name, time, width, height, seed])

        # save new data and apply changes to screen
        self.save()
        self.rescale()


class Start(Ui_Screen):
    def __init__(self, game):
        super().__init__(game)

        # init elements
        self.start_text = MS.Text(game, default_rect(), "Start Level")
        self.elements.add(self.start_text)
        self.label_text = MS.Text(game, default_rect(), "Maze Size:")
        self.elements.add(self.label_text)
        self.width_text = MS.Text(game, default_rect(), "Width:")
        self.elements.add(self.width_text)
        self.height_text = MS.Text(game, default_rect(), "Height:")
        self.elements.add(self.height_text)
        self.cross_text = MS.Text(game, default_rect(), "X")
        self.elements.add(self.cross_text)
        self.seed_text = MS.Text(game, default_rect(), "Seed:")
        self.elements.add(self.seed_text)
        self.width_i = MS.Input_Box(game, default_rect(), "20", MS.k2c_numeric)
        self.elements.add(self.width_i)
        self.height_i = MS.Input_Box(game, default_rect(), "10", MS.k2c_numeric)
        self.elements.add(self.height_i)
        self.seed_i = MS.Input_Box(game, default_rect(), "0", MS.k2c_numeric)
        self.elements.add(self.seed_i)
        self.start_b = MS.Button(game, default_rect(), "Start Level")
        self.elements.add(self.start_b)
        self.exit_b = MS.Button(game, default_rect(), "Cancel")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()

    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # start level button
        if self.start_b.falling_edges[0]:
            # get width
            if len(self.width_i.text) > 0:
                width = int(self.width_i.text)
            else:
                width = int(self.width_i.default_text)

            # width validation
            if not 10 <= width <= 50:
                self.game.snd_loader.get("spinner end").play()
                self.width_i.text = ""
                self.width_i.rescale()
                return

            # get height
            if len(self.height_i.text) > 0:
                height = int(self.height_i.text)
            else:
                height = int(self.height_i.default_text)
            
            # height validation
            if not 10 <= height <= 50:
                self.game.snd_loader.get("spinner end").play()
                self.height_i.text = ""
                self.height_i.rescale()
                return

            # get seed
            if len(self.seed_i.text) > 0:
                seed = int(self.seed_i.text)
            else:
                seed = int(self.seed_i.default_text)

            # start level
            self.game.start_level((width, height), seed)

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.game_state_stack.pop(-1)
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack.pop(-1)
                break

    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.start_text.rect.width = screen_size.x
        self.start_text.rect.height = screen_size.y / 10
        self.start_text.rect.centerx = screen_rect.centerx
        self.start_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 12
        button_pos_y = screen_size.y * 1 / 4

        # maze size text
        self.label_text.rect.width = button_width
        self.label_text.rect.height = button_height
        self.label_text.rect.centerx = screen_rect.centerx
        self.label_text.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # width and height text
        width_x = screen_rect.centerx - screen_size.x / 6
        height_x = screen_rect.centerx + screen_size.x / 6
        dim_width = button_width * 3/4

        self.width_text.rect.width = button_width
        self.width_text.rect.height = button_height
        self.width_text.rect.centerx = width_x
        self.width_text.rect.centery = button_pos_y

        self.height_text.rect.width = button_width
        self.height_text.rect.height = button_height
        self.height_text.rect.centerx = height_x
        self.height_text.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # width and height inputs
        self.width_i.rect.width = dim_width
        self.width_i.rect.height = button_height
        self.width_i.rect.centerx = width_x
        self.width_i.rect.centery = button_pos_y

        self.height_i.rect.width = dim_width
        self.height_i.rect.height = button_height
        self.height_i.rect.centerx = height_x
        self.height_i.rect.centery = button_pos_y

        # X
        self.cross_text.rect.width = screen_size.x / 20
        self.cross_text.rect.height = button_height
        self.cross_text.rect.centerx = screen_rect.centerx
        self.cross_text.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # seed input
        self.seed_text.rect.width = button_width * 1/2
        self.seed_text.rect.height = button_height
        self.seed_text.rect.centerx = screen_rect.centerx - button_width * 3/8
        self.seed_text.rect.centery = button_pos_y

        self.seed_i.rect.width = button_width * 3/4
        self.seed_i.rect.height = button_height
        self.seed_i.rect.centerx = screen_rect.centerx + button_width * 1/4
        self.seed_i.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # randomise seed
        rng.seed()
        self.seed_i.default_text = str(rng.randint(0,999999))
        
        # start button
        self.start_b.rect.width = button_width
        self.start_b.rect.height = button_height
        self.start_b.rect.centerx = screen_rect.centerx
        self.start_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = button_width
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # call parent rescale method
        super().rescale()


class End(Ui_Screen):
    def __init__(self, game, time, width, height, seed):
        super().__init__(game)
        self.score_added = False
        self.time = time
        self.width = width
        self.height = height
        self.seed = seed

        # init elements
        self.end_text = MS.Text(game, default_rect(), "Level Complete!")
        self.elements.add(self.end_text)
        self.dim_text = MS.Text(game, default_rect(), f"{width:^8}X{height:^8}")
        self.elements.add(self.dim_text)
        self.seed_text = MS.Text(game, default_rect(), f"Seed:{seed:^8}")
        self.elements.add(self.seed_text)
        self.Time_text = MS.Text(game, default_rect(), f"Time:{time:^8}")
        self.elements.add(self.Time_text)

        self.sb1_text = MS.Text(game, default_rect(), 
                                "Put Your Name on")
        self.elements.add(self.sb1_text)
        self.sb2_text = MS.Text(game, default_rect(), 
                                "The Scoreboard!:")
        self.elements.add(self.sb2_text)

        self.name_i = MS.Input_Box(game, default_rect(), "Enter Name", 
                                    MS.k2c_numeric + 
                                    MS.k2c_alpha_lower + 
                                    MS.k2c_alpha_upper + 
                                    [" "])
        self.elements.add(self.name_i)

        self.add_b = MS.Button(game, default_rect(), "Add To Scoreboard")
        self.elements.add(self.add_b)

        self.exit_b = MS.Button(game, default_rect(), "Return to Main Menu")
        self.elements.add(self.exit_b)

        # load background
        self.background = game.img_loader.get("menu background")

        # call rescale to render image
        self.rescale()

    def tick(self, events, dt):
        # call parent tick method
        super().tick(events, dt)

        # add to scoreboard
        if not self.score_added and self.add_b.falling_edges[0]:
            if len(self.name_i.text) > 0:
                self.score_added = True
                self.game.scoreboard_screen.add_score(self.name_i.text, 
                                                      self.time,
                                                      self.width,
                                                      self.height,
                                                      self.seed)
                self.add_b.text_colour = (128,128,128)
                self.add_b.rescale()

        # exit button
        if self.exit_b.falling_edges[0]:
            self.game.game_state_stack = [self.game.main_screen.tick]
        # ESC key
        for event in events:
            if event.type == pg.KEYUP and event.key == pg.K_ESCAPE:
                self.game.game_state_stack = [self.game.main_screen.tick]
                break


    def rescale(self):
        screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())
        screen_size = vec2(screen_rect.size)

        # positon title text
        self.end_text.rect.width = screen_size.x
        self.end_text.rect.height = screen_size.y / 10
        self.end_text.rect.centerx = screen_rect.centerx
        self.end_text.rect.centery = screen_size.y / 8

        # position buttons
        button_width = screen_size.x / 3
        button_height = screen_size.y / 14
        button_spacing = screen_size.y / 6
        button_pos_y = screen_size.y * 1 / 3

        left_column = screen_size.x * 1/4
        right_column = screen_size.x * 3/4

        # maze size text
        self.dim_text.rect.width = screen_size.x * 1/2
        self.dim_text.rect.height = button_height
        self.dim_text.rect.centerx = left_column
        self.dim_text.rect.centery = button_pos_y

        # add to scoreboard text
        self.sb1_text.rect.width = screen_size.x * 1/2
        self.sb1_text.rect.height = button_height * 2/3
        self.sb1_text.rect.centerx = right_column
        self.sb1_text.rect.centery = button_pos_y 

        self.sb2_text.rect.width = screen_size.x * 1/2
        self.sb2_text.rect.height = button_height * 2/3
        self.sb2_text.rect.centerx = right_column
        self.sb2_text.rect.centery = button_pos_y + button_spacing / 3
        button_pos_y += button_spacing 

        # seed text
        self.seed_text.rect.width = screen_size.x * 1/2
        self.seed_text.rect.height = button_height
        self.seed_text.rect.centerx = left_column
        self.seed_text.rect.centery = button_pos_y

        # name input
        self.name_i.rect.width = screen_size.x * 1/2
        self.name_i.rect.height = button_height
        self.name_i.rect.centerx = right_column
        self.name_i.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # time text
        self.Time_text.rect.width = screen_size.x * 1/2
        self.Time_text.rect.height = button_height
        self.Time_text.rect.centerx = left_column
        self.Time_text.rect.centery = button_pos_y

        # add name button
        self.add_b.rect.width = screen_size.x * 1/2
        self.add_b.rect.height = button_height
        self.add_b.rect.centerx = right_column
        self.add_b.rect.centery = button_pos_y
        button_pos_y += button_spacing

        # exit button
        self.exit_b.rect.width = screen_size.x * 2/3
        self.exit_b.rect.height = button_height
        self.exit_b.rect.centerx = screen_rect.centerx
        self.exit_b.rect.centery = button_pos_y

        # call parent rescale method
        super().rescale()


class Level(Ui_Screen):
    def __init__(self, game, size, seed):
        super().__init__(game)
        self.size = size
        self.seed = seed
        self.timer = sprites.Timer(self.game)
        self.win_snd = game.snd_loader.get("winfretless.ogg")
    
    def setup(self):
        """sets up the level"""
        # initialise camera
        self.camera = sprites.Camera(self.game)

        # start setting up the maze
        self.maze = mg.Maze(self.game, self.size, self.seed) 
        # finishes generating the maze and sprites
        self.maze.setup()
        # initalise sprites in maze
        for sprite in self.maze.all_sprites:
                sprite.render(0)

        # initialise player
        self.player = sprites.Player(self.game, (self.maze.start))
        self.maze.all_sprites.add(self.player)
        # set what the camera should follow
        self.camera.set_target(self.player)
        self.camera.pos = pg.Vector2(5,5)

        self.rescale()

    def tick(self, events, dt):
        super().tick(events, dt)
        self.game.screen.fill((255,0,255))

        for event in events:
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    self.game.game_state_stack.append(
                        self.game.pause_screen.tick)
                # if event.key == pg.K_SPACE:
                #     self.game.end_level((20,10), 12345, 678)

            # zoom debug
            # if event.type == pg.MOUSEBUTTONDOWN:
            #     if event.button == 4:
            #         self.camera.zoom = min(self.camera.zoom+1, 20)
            #     if event.button == 5:
            #         self.camera.zoom = max(self.camera.zoom-1 , 1)
            #     self.rescale()
        
        # update all sprites
        self.maze.all_sprites.update(dt)
        self.camera.update(dt)
        self.timer.update(dt)

        # detect win condition:
        if (self.player.pos+vec2(0.25,0.75))//1 == self.maze.exit.pos:
            self.win_snd.play()
            self.game.end_level(self.size, self.seed, self.timer.total_time)

        # call all sprites render method
        for sprite in self.maze.all_sprites:
            sprite.render(dt)

        self.game.screen.fill((32,32,32))
        # draw floor in correct position
        for y in range(0, self.maze.bsize[1]-1, 5):
            for x in range(0, self.maze.bsize[0]-1, 5):
                self.floor_rect.topleft = self.camera.wrld_2_scrn_coord((x,y))
                if self.floor_rect.colliderect(self.screen_rect):
                    self.screen.blit(self.floor, self.floor_rect)

        self.maze.all_sprites.draw(self.game.screen)

    def rescale(self):
        self.screen_rect = pg.rect.Rect(0, 0, *self.screen.get_size())

        # rescale background
        floor = self.game.img_loader.get("arcade_carpet_1_512")
        floor_size = self.camera.wrld_2_scrn_coord((5,5)) - \
                     self.camera.wrld_2_scrn_coord((0,0))
        self.floor = pg.transform.scale(floor, floor_size)
        self.floor_rect = self.floor.get_rect()

        super().rescale()

