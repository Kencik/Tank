#! /home/kent/anaconda3/bin/python3
import sys, os
import pygame
from pygame.locals import *
from SpriteSheetLoader import ImageLoader
from Wall import Wall
from levelManager import LevelManager
from menuManager import MenuManager
import Levels

class TankMain:
    #Glowna klasa programu - zawiera funkcje tworzaca ekran, petle glowno gry etc...
    
    def __init__(self, width = 300, height = 240):
        
        self.multiplier = 1
        
        #Wczytaj ustawienia z pliku
        self.loadSettings()
        
        #Zapisz ustawienia rozmiaru ekranu
        self.baseWidth = width
        self.baseHeight = height
        self.width = width*self.multiplier
        self.height = height*self.multiplier
        self.imageTileSize = 16
        self.tileSize = self.imageTileSize*self.multiplier
        self.offset_x = (self.width - self.tileSize*15)/2
        self.offset_y = (self.height - self.tileSize*15)/2
        self.levelNumber = 1
        
        #Inizjalizacja pygame i stworzenie okna
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tank')
        
        self.menuManager = MenuManager(self.screen, self.tileSize, self.imageTileSize)
        
    def main(self):
        
        choice = self.menuLoop()
        if choice == 0:
            for level in Levels.levels:
                self.displayStageInfo(self.levelNumber)
                if self.levelLoop(level):
                    self.levelNumber += 1
                else:
                    break
            self.levelNumber = 1
        if choice == 1 or choice == 2:
         
            #Zapisz ustawienia rozmiaru ekranu
            self.multiplier = choice
            self.width = self.baseWidth * self.multiplier
            self.height = self.baseHeight * self.multiplier
            self.tileSize = self.imageTileSize*self.multiplier
            self.offset_x = (self.width - self.tileSize*15)/2
            self.offset_y = (self.height - self.tileSize*15)/2
            
            #Ponadto zapisz je do pliku settings
            self.saveSettings()
            
            #Inizjalizacja pygame i stworzenie okna
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            
            self.menuManager = MenuManager(self.screen, self.tileSize, self.imageTileSize)
            #self.levelManager = LevelManager(Levels.level1, self.tileSize, self.imageTileSize, self.offset_x, self.offset_y)
            
        self.main()
        
    def levelLoop(self, level):
        
        self.levelManager = LevelManager(level, self.tileSize, self.imageTileSize, self.offset_x, self.offset_y)
        
        #Stworz tlo
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        
        while 1:
            #Ustaw liczbe klatek na sekunde
            clock = pygame.time.Clock()
            clock.tick(60)
            
            #Sprawdz czy nadeszly jakies zdarzenia
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN)):
                        self.levelManager.startMove(event.key)
                    if event.key == K_SPACE:
                        self.levelManager.shootRequest()
                elif event.type == KEYUP:
                    if ((event.key == K_RIGHT) or (event.key == K_LEFT) or (event.key == K_UP) or (event.key == K_DOWN)):
                        self.levelManager.stopMove(event.key)
            
            #Porusz co trzeba na planszy jesli trzeba
            self.levelManager.update()
        
            #Rendering
            self.screen.blit(self.background, (0, 0)) 
            self.levelManager.render(self.screen)
            
            #Sprawdz czy gracz wygral
            if self.levelManager.levelWon:
                return True
            
            #Sprawdz czy gracz przegral
            if self.levelManager.gameOver:
                self.displayGameOver()
                return False
                
                    
            pygame.display.flip()
            
    def menuLoop(self):
        #Stworz tlo
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        
        sound = pygame.mixer.Sound('sounds/button.wav')
        
        while 1:
            #Ustaw liczbe klatek na sekunde
            clock = pygame.time.Clock()
            clock.tick(60)
            
            #Sprawdz czy nadeszly jakies zdarzenia
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        sound.play()
                        return self.menuManager.pointer
                    if event.key == K_UP:
                        self.menuManager.pointer = (self.menuManager.pointer - 1) % 3 
                    if event.key == K_DOWN:
                        self.menuManager.pointer = (self.menuManager.pointer + 1) % 3

            self.menuManager.update()
            self.screen.blit(self.background, (0, 0)) 
            self.menuManager.render()
            
            pygame.display.flip()
            
    def displayStageInfo(self, number):
        loader = ImageLoader(multiplier = self.multiplier)
        backgroundImage = loader.getImage((23*self.imageTileSize, 0, self.imageTileSize, self.imageTileSize))
        color = backgroundImage.get_at((0,0))
        
        stageImage = loader.getImage((20.5*self.imageTileSize, 11*self.imageTileSize, 2.5*self.imageTileSize, 0.5*self.imageTileSize))
        
        if number == 1:
            numbImage = loader.getImage((self.imageTileSize*21, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        if number == 2:
            numbImage = loader.getImage((self.imageTileSize*21.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        if number == 3:
            numbImage = loader.getImage((self.imageTileSize*22, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        if number == 4:
            numbImage = loader.getImage((self.imageTileSize*22.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        
        #Stworz tlo
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill(color)
        
        center1 = ((self.width - stageImage.get_width())/2, (self.height - stageImage.get_height())/2)
        center2 = (center1[0] + 50*self.multiplier, center1[1])
        
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(stageImage, center1)
        self.screen.blit(numbImage, center2)
        pygame.display.flip()
        pygame.time.wait(1000)
        
    def displayGameOver(self):
        sound = pygame.mixer.Sound('sounds/gameover.wav')
        loader = ImageLoader(multiplier = self.multiplier)
        GAME_OVER_IMAGE = loader.getImage((18*self.imageTileSize, 11.5*self.imageTileSize, 2*self.imageTileSize, self.imageTileSize), -1)
        center = ((self.width - 2*self.imageTileSize)/2, (self.height - self.imageTileSize)/2)
        
        self.screen.blit(GAME_OVER_IMAGE, center)
        sound.play()
        pygame.display.flip()
        pygame.time.wait(2000)
        
    def loadSettings(self):
        plik = open('settings').readlines()
        for line in plik:
            line = line.split()
            if line[0] == 'window_size':
                if line[2] == '600:480':
                    self.multiplier = 2
                elif line[2] == '300:240':
                    self.multiplier = 1
    
    def saveSettings(self):
        sizeStr = 'window_size = ' + str(self.baseWidth*self.multiplier) + ":" + str(self.baseHeight*self.multiplier)
        print(sizeStr)
        
        zrodlo = open('settings').readlines()
        cel = open('settings', 'w')
        
        for line in zrodlo:
            lineList = line.split()
            if lineList[0] == 'window_size':
                cel.write(line.replace(line, sizeStr))
                
        cel.close()
                
        
if __name__ == "__main__":
    MainWindow = TankMain()
    MainWindow.main()