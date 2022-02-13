import pygame as pg

class dummy_parent_screen():
    def __init__(self, game):
        self.game = game

    def tick(self, event_list, dt):
        print(f"{self.__class__.__name__} screen")
        pg.time.delay(1000)
        self.game.game_state_stack.pop(-1)

    def rescale(self):
        print(f"{self.__class__.__name__} rescaled")

class Main(dummy_parent_screen):
    def __init__(self, game):
        self.game = game

    def tick(self, event_list, dt):
        pass
        # match input("next screen: ").split(" "):
        #     case ["start"]:
        #         s = self.game.start_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["level"]:
        #         s = self.game.level.tick
        #         self.game.game_state_stack.append(s)
        #     case ["end"]:
        #         s = self.game.end_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["scoreboard"]:
        #         s = self.game.scoreboard_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["pause"]:
        #         s = self.game.pause_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["options"]:
        #         s = self.game.options_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["gfx"]:
        #         s = self.game.gfx_options_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["snd"]:
        #         s = self.game.snd_options_screen.tick
        #         self.game.game_state_stack.append(s)
        #     case ["level_init", w, h, seed]:
        #         self.game.start_level((int(w),int(h)), int(seed))
        #     case _:
        #         print("pattern not recognised")
                

class Pause(dummy_parent_screen):
    pass

class Options(dummy_parent_screen):
    pass
    
class GFX_Options(dummy_parent_screen):
    pass

class SND_Options(dummy_parent_screen):
    pass

class Scoreboard(dummy_parent_screen):
    pass

class Start(dummy_parent_screen):
    pass

class End(dummy_parent_screen):
    pass

class Level(dummy_parent_screen):
    def __init__(self, game, size, seed):
        super().__init__(game)
        print(f"level, size:{size}, seed:{seed} created")