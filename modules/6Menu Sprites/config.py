import re
from pathlib import Path


class Config():
    def __init__(self):
        # file paths: they are in reference to the game root foolder
        self.img_path = (Path(__file__).parent / 'img').as_posix()
        self.snd_path = (Path(__file__).parent / 'snd').as_posix()
        self.music_path = 'snd/music'
        self.scoreboard_path = 'scoreboard.csv'

        # graphics config
        self.resolution = (1600, 900)
        self.rescaleable = True
        self.fullscreen = False
        self.vsync = True
        self.colours = [(0xAC, 0x32, 0x32),
                        (0xDF, 0x71, 0x26),
                        (0x99, 0XE5, 0X50),
                        (0X00, 0X50, 0xEF),
                        (0X76, 0X42, 0X8A),
                        (0X00, 0XCC, 0XCC)]
        self.camera_zoom = 10
        self.key_frame_count = 10
        self.key_displacement = 4

        # sound
        self.game_vol = 1.0
        self.music_vol = 0.3
        self.player_step_snd_delay = 300

        # fonts
        self.text_colour = (255,255,255)
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

    # self modifying code: save the attributes  by rewriting this file
    def save(self):
        self_file = open(__file__, "r")
        self_file_str = self_file.read()
        self_file.close()

        for identifier, val in self.__dict__.items():
            self_file_str = re.sub(f" self.{identifier} = .+\n",
                                   f" self.{identifier} = {repr(val)}\n",
                                   self_file_str)

        self_file = open(__file__, "w")
        self_file.write(self_file_str)
        self_file.close()
