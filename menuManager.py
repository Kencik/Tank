import pygame
from pygame.locals import *
from SpriteSheetLoader import ImageLoader
from GameObject import GameObject, AnimatedGameObject

class MenuManager:
    
    def __init__(self, screen, tileSize, imageTileSize):
        self.screen = screen
        self.size = self.screen.get_size()
        self.tileSize = tileSize
        self.imageTileSize = imageTileSize
        self.multiplier = self.tileSize/self.imageTileSize
        
        self.pointer = 0
        
        self.loadSprites()
        
    def loadSprites(self): 
        #Wczytaj i zapisz do sprite'a obrazek z logo gry
        self.loader = ImageLoader("menu.png", self.multiplier)
        self.BATTLE_CITY_IMAGE = self.loader.getImage((0, 30, 256, 80))
        centerPoint = (self.screen.get_size()[0]/2, 50*self.multiplier)
        battleCity = GameObject((centerPoint), self.BATTLE_CITY_IMAGE)
        self.battleCitySprite = pygame.sprite.RenderPlain(battleCity)
        
        #Obrazek odpowiadajacy wyborowi menu ktory rozpoczyna gre
        x = 147*self.multiplier
        y = 120*self.multiplier
        
        self.START_GAME_IMAGE = self.loader.getImage((80, 120, 80, 20))
        startGame = GameObject((x, y), self.START_GAME_IMAGE)
        self.startGameSprite = pygame.sprite.RenderPlain(startGame)
        
        self.loader.setSheet("SpriteSheet.png")
        
        #Obrazek czolgu ktory jest wskaznikiem wyboru w menu
        self.POINTER_IMAGE = self.loader.getImage((self.imageTileSize*7, 0, self.imageTileSize, self.imageTileSize), -1)
        self.pointerObject = GameObject((x - 45*self.multiplier, y), self.POINTER_IMAGE)
        self.pointerSprite = pygame.sprite.RenderPlain(self.pointerObject)
        
        #Obrazki do elementow menu, sluzacych do zmiany rozmiaru ekranu
        self.NUMBER_0 = self.loader.getImage((self.imageTileSize*20.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_1 = self.loader.getImage((self.imageTileSize*21, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_2 = self.loader.getImage((self.imageTileSize*21.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_3 = self.loader.getImage((self.imageTileSize*22, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_4 = self.loader.getImage((self.imageTileSize*22.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_5 = self.loader.getImage((self.imageTileSize*20.5, 12*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_6 = self.loader.getImage((self.imageTileSize*21, 12*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_7 = self.loader.getImage((self.imageTileSize*21.5, 12*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_8 = self.loader.getImage((self.imageTileSize*22, 12*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_9 = self.loader.getImage((self.imageTileSize*22.5, 12*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        
        x = (self.size[0] - 7*self.tileSize/2)/2
        y += self.tileSize
        num1 = GameObject((x, y), self.NUMBER_3)
        num2 = GameObject((x+self.tileSize/2, y), self.NUMBER_0)
        num3 = GameObject((x+2*self.tileSize/2, y), self.NUMBER_0)
        num4 = GameObject((x+4*self.tileSize/2, y), self.NUMBER_2)
        num5 = GameObject((x+5*self.tileSize/2, y), self.NUMBER_4)
        num6 = GameObject((x+6*self.tileSize/2, y), self.NUMBER_0)
        self.str1 = pygame.sprite.Group()
        self.str1.add(num1)
        self.str1.add(num2)
        self.str1.add(num3)
        self.str1.add(num4)
        self.str1.add(num5)
        self.str1.add(num6)

        y += self.tileSize
        num1 = GameObject((x, y), self.NUMBER_6)
        num2 = GameObject((x+self.tileSize/2, y), self.NUMBER_0)
        num3 = GameObject((x+2*self.tileSize/2, y), self.NUMBER_0)
        num4 = GameObject((x+4*self.tileSize/2, y), self.NUMBER_4)
        num5 = GameObject((x+5*self.tileSize/2, y), self.NUMBER_8)
        num6 = GameObject((x+6*self.tileSize/2, y), self.NUMBER_0)
        self.str2 = pygame.sprite.Group()
        self.str2.add(num1)
        self.str2.add(num2)
        self.str2.add(num3)
        self.str2.add(num4)
        self.str2.add(num5)
        self.str2.add(num6)
        
    def update(self):
        x = 102*self.multiplier
        y = 120*self.multiplier
        
        if self.pointer == 0:
            self.pointerObject.rect.center = (x,y)
        elif self.pointer == 1:
            self.pointerObject.rect.center = (x, y+self.tileSize)
        elif self.pointer == 2:
            self.pointerObject.rect.center = (x, y+2*self.tileSize)
        
    def render(self):
        self.battleCitySprite.draw(self.screen)
        self.startGameSprite.draw(self.screen)
        self.pointerSprite.draw(self.screen)
        self.str1.draw(self.screen)
        self.str2.draw(self.screen)