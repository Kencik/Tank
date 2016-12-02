import pygame
 
class GameObject(pygame.sprite.Sprite):
#Klasa bedaca podstawowym modelem kazdego obiektu w grze.
     
    def __init__(self, centerPoint, image):
        #Konstruktor klasy Sprite
        pygame.sprite.Sprite.__init__(self)
        
        #Ustaw obrazek, prostokat (potrzebny do wykrywania kolizji) i polozenie srodka
        self.image = image
        self.rect = image.get_rect()
        self.rect.center = centerPoint
        
    def changeImage(self, image):
        self.image = image
        
class AnimatedGameObject(GameObject):
#Rozszerzona klasa GameObject przeznaczona dla obiektow gry nieruchomych, ale posiadajacych animacje
    
    def __init__(self, centerPoint, images, framesPerImage):
        GameObject.__init__(self, centerPoint, images[0])
        
        self.FRAMES_PER_IMAGE = framesPerImage
        self.images = images
        
        self.currentImage = 0
        self.animation_it = 0
        
    def update(self):
    #Zwraca True jesli to juz koniec wybuchu
        self.animation_it += 1
        
        if self.animation_it == self.FRAMES_PER_IMAGE:
            if self.currentImage == len(self.images) -1:
                return True
            self.currentImage += 1
            self.animation_it = 0
            
        self.image = self.images[self.currentImage]
        return False