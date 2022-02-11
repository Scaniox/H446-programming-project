# load config
import config


# prints all attributes of a config object
def print_config_vals(cfg):
    for id, val in game_config.__dict__.items():
        print(f"id:{str(id):<40}, " +
              f"val:{str(val):<20}, " +
              f"type:{str(type(val)):<15}")


# init config
game_config = config.Config()

# load and print all values from config
print_config_vals(game_config)

# make changes to values
game_config.snd_path = "other_snd_path"
game_config.player_max_speed = 30
game_config.vsync = True
game_config.music_vol = 0.3
game_config.text_colour = (123, 45, 67)

# save changes
game_config.save()

# reload config
del config
import config

# reinit config
game_config = config.Config()

# print all values from config
print("\n\n\nconfig reloaded: ")
print_config_vals(game_config)
