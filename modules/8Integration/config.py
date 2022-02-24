import re
from pathlib import Path
import sys


class Config():
    def __init__(self):

        # get file paths
        if getattr(sys, 'frozen', False):
            # is running in exe
            if hasattr(sys, '_MEIPASS'):
                app_path = Path(sys._MEIPASS)
                exe_parent_path = Path(sys.executable).parent
            else:
                print("can't find local path")
                input()
        else:
            # is running in python interpreter
            app_path = Path(__file__).parent
            exe_parent_path = app_path

            
        print(f"local path: {app_path}, exe parent path: {exe_parent_path}")

        # file paths: they are in reference to the game root foolder
        self.img_pathX = (app_path / 'img').as_posix()
        self.snd_pathX = (app_path / 'snd').as_posix()
        self.scoreboard_pathX = (exe_parent_path / 'scoreboard.csv').as_posix()
        self.settings_save_pathX = (exe_parent_path / 'settings.set')

        # graphics config
        self.resolution = [1366, 768]
        self.rescaleable = False
        self.fullscreen = False
        self.vsync = True
        self.coloursX = [(0xAC, 0x32, 0x32),
                        (0xDF, 0x71, 0x26),
                        (0x99, 0XE5, 0X50),
                        (0X00, 0X50, 0xEF),
                        (0X76, 0X42, 0X8A),
                        (0X00, 0XCC, 0XCC)]
        self.camera_zoom = 10
        self.key_frame_count = 10
        self.key_displacement = 4

        # sound
        self.game_vol = 1
        self.music_vol = 0.25
        self.player_step_snd_delay = 300

        # fonts
        self.text_colour = (255, 255, 255)
        self.text_font_name = 'PixeloidMono-1G8ae.ttf'

        # walking sprites
        self.player_hurt_cooldown = 500
        self.player_max_health = 5
        self.player_max_speed = 0.05
        self.player_acc = 0.3
        self.enemy_speed = 0.02

        # maze generation
        self.maze_blocks_start_proportion = 0.08333333333333333
        self.maze_blocks_distance_proportion = 0.16666666666666666
        self.maze_gateway_jitter = 0
        self.maze_gateway_skip_threshold = 0.2
        self.maze_branch_stop_threshold = 0.05
        self.maze_key_count = 6
        self.maze_checkpoint_count = 5
        self.maze_enemy_count = 6
        self.walls_width_px = 16
        self.walls_height_px = 24

        self.load()

    def save(self):
        """saves settings"""
        save_file_str = ""
        for identifier, val in self.__dict__.items():
            if identifier[-1] != "X":
                save_file_str += f"{identifier}|{repr(val)}\n"

        save_file = open(self.settings_save_pathX, "w")
        save_file.write(save_file_str)
        save_file.close()

    def load(self):
        """loads settings"""
        try:
            save_file = open(self.settings_save_pathX, "r")
        except:
            return

        for line in save_file.readlines():
            if "|" in line:
                id, val = line.strip().split("|")
                exec(f"self.{id} = {val}")

        save_file.close()