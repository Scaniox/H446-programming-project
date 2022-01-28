import pygame
from pygame.locals import *

import math
import numpy

pygame.mixer.pre_init(44100, -16, 2)
pygame.mixer.init()

buf = numpy.zeros((44100, 2), dtype = numpy.int16)
for s in range(44100):
    buf[s] = [int(round(32767*math.sin(2*math.pi*400*float(s)/44100)))]*2

sound = pygame.sndarray.make_sound(buf)
#play once, then loop forever
sound.play(loops = 0)

input()

pygame.quit()

# dependent on numpy
