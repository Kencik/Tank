import pygame
import GameObject

class Wall(GameObject.GameObject):
    #To jest klasa reprezentujaca kafelek sciany, ktory moze ulec zniszczeniu
    
    def __init__(self, centerPoint, image):
        GameObject.GameObject.__init__(self, centerPoint, image)
        
        """Definiujemy 4 dodatkowe obiekty gry w ramach scianach, ktore beda nam sluzyly jako collidery, 
            po to zeby mozna bylo zniszczyc czesc sciany"""
            
        #Zmienne pomocnicze do stworzenie prostokatow
        x = self.rect.left
        y = self.rect.top
        x_off = self.rect.width/4
        y_off = self.rect.height/4
        
        self.wallFragments = []
        
        #Tworze prostokaty fragmentow sciany
        for i in range(4):
            for j in range(4):
                rect = pygame.Rect(j*x_off, i*y_off, x_off, y_off)
                rectImage = pygame.Surface(rect.size).convert()
                rectImage.blit(self.image, (0,0), rect)
                self.wallFragments.append(GameObject.GameObject((x+(2*j+1)*x_off/2, y+(2*i+1)*y_off/2), rectImage))
        topLeftRect = pygame.Rect(0, 0, x_off, y_off)
        topRightRect = pygame.Rect(x_off, 0, x_off, y_off)
        bottomLeftRect = pygame.Rect(0, y_off, x_off, y_off)
        bottomRightRect = pygame.Rect(x_off, y_off, x_off, y_off)
        
    def getWallCorners(self):
        return self.wallFragments
