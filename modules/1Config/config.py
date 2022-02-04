import re

class Config():
    def __init__(self):
        # file paths: they are in reference to the game root foolder
        self.img_path = "img"
        self.snd_path = "snd"
        self.music_path = "snd/music"
        self.scoreboard_path = "scoreboard.csv"

        self.resolution = (640,480)
        self.fullscreen = False
        self.vsync = False

        self.game_vol = 1.0
        self.music_vol = 1.0

        self.text_colour = (192,192,192)
        self.text_font_name = "Pixeloid"

        self.player_hurt_cooldown = 500
        self.player_max_health = 100
        self.player_max_speed = 20
        self.player_acc = 2
        self.enemy_speed = 10

        self.maze_blocks_start_proportion = 1/12
        self.maze_blocks_distance_proportion = 1/6
        self.maze_gateway_jitter = 6
        self.maze_gateway_skip_threshold = 0.3
        self.maze_branch_stop_threshold = 0.1
        self.maze_key_count = 6
        self.maze_checkpoint_count = 10
        self.maze_enemy_count = 4

    def save(self): # self modifying code: save the attributes to this file
        self_file = open(__file__, "r")
        self_file_str = self_file.read()
        self_file.close()

        for identifier, val in self.__dict__.items():
            self_file_str = re.sub(f" self\.{identifier} = .+\n", \
                                   f" self.{identifier} = {repr(val)}\n", \
                                   self_file_str)

        self_file = open(__file__, "w")
        self_file.write(self_file_str)
        self_file.close()
