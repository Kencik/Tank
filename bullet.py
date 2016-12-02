import pygame
from pygame.locals import *
from GameObject import GameObject

class bullet(GameObject):
    
    def __init__(self, centerPoint, images, tileSize, direction):
        GameObject.__init__(self, centerPoint, images[0])
        
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4
        
        self.PIXEL_PER_FRAME = tileSize/8
        
        self.image1 = images[0]
        self.image2 = images[1]
        self.image3 = images[2]
        self.image4 = images[3]
