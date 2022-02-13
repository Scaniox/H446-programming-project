import pygame as pg
import config
import Asset_Loader as AL

class Game():
    def __init__(self):
        # initialise pygame
        pg.init()
        self.screen = pg.display.set_mode((1000, 800))

        # init config
        self.config = config.Config()

        # init loaders
        self.img_loader = AL.Img_Loader(self)
        self.snd_loader = AL.Snd_Loader(self)

        # fill screen with dark green
        self.screen.fill((0, 128, 0))
        
        # load and render img1.png
        img1 = self.img_loader.get("img1.png")
        new_size = [i*8 for i in img1.get_size()]
        self.screen.blit(pg.transform.scale(img1, new_size), (10,10))

        # load "block light blue"
        sprite1 = self.img_loader.get("block light blue")
        new_size = [i*8 for i in sprite1.get_size()]
        self.screen.blit(pg.transform.scale(sprite1, new_size), (150,10))

        # re load img1.png
        img1 = self.img_loader.get("img1.png")
        new_size = [i*8 for i in img1.get_size()]
        self.screen.blit(pg.transform.scale(img1, new_size), (300,10))

        # load img2.png
        # re load img1.png
        img1 = self.img_loader.get("img2.png")
        new_size = [128,128]
        self.screen.blit(pg.transform.scale(img1, new_size), (450,10))

        # flip so that sprites are rendered to screen
        pg.display.flip()

        # load sound1.wav
        snd1 = self.snd_loader.get("sound1.wav")
        snd1.play(10)

        # delay between sounds
        pg.time.delay(round(snd1.get_length()*1000 *10))

        # load sound2.wav
        snd2 = self.snd_loader.get("sound2.wav")
        snd2.play(10)

        # wait for user input to close
        input()

        pg.quit()

Game()