import pygame

class ImageLoader:
    "Klasa przechowujaca spriteSheet z wszystkimi grafikami. Pozwala pobierac poszczegolne obrazki."
    
    def __init__(self, name = "SpriteSheet.png", multiplier = 2):
        self.sheet = pygame.image.load(name).convert()
        self.multiplier = multiplier
    
    def setSheet(self, name):
        self.sheet = pygame.image.load(name).convert()
    
    def getImage(self, rectangle, colorkey=None):
        "Laduje obrazek z konkretnego prostokata w spriteSheet."
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0,0), rect)
        width = image.get_width() * self.multiplier
        height = image.get_height() * self.multiplier
        image = pygame.transform.scale(image, (int(width), int(height)))
        
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
