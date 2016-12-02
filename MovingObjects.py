import pygame
from pygame.locals import *
from GameObject import GameObject, AnimatedGameObject

class MovingObject(GameObject):
    
    def __init__(self, centerPoint, images, tileSize, framesPerMove, direction = 1, moveLength = 0):
        GameObject.__init__(self, centerPoint, images[0])
        
        self.UP = 1
        self.DOWN = 2
        self.LEFT = 3
        self.RIGHT = 4
        
        #Zmienna informujaca ile klatek musi minac nim zostanie wykonany pojedynczy ruch (tzn o pol rozmiaru tileSize)
        self.FRAMES_PER_MOVE = framesPerMove
        
        #Ile pikseli ruszamy sie w jednej iteracji animacji
        if not moveLength:
            moveLength = tileSize/4
        self.PIXELS_PER_FRAME = (moveLength)/self.FRAMES_PER_MOVE
        
        #Aktualny kierunek 
        self.direction = direction
        
        #Czy obiekt jest aktualnie w trakcie animacji
        self.isMoving = False
        
        #Iterator animacji
        self.animation_it = 0
        
        self.image1 = images[0]
        self.image2 = images[1]
        self.image3 = images[2]
        self.image4 = images[3]
        
        #Ustaw obrazek
        if self.direction == self.UP:
            self.image = self.image1
        if self.direction == self.DOWN:
            self.image = self.image2
        if self.direction == self.LEFT:
            self.image = self.image3
        if self.direction == self.RIGHT:
            self.image = self.image4
            
        self.centerPoint = centerPoint
        self.direction = self.UP
    
    def update(self):
        if self.isMoving:
            # Bez wzgledu na wszystko, jesli czolg jest w trakcie cyklu animacji (tzn pomiedzy kolejnymi dyskretnymi punktami
            # po ktorych moze sie poruszac)to kontynuuj te animacje i nie rob nic wiecej
            self.animation_it += 1
            if self.direction == self.UP:
                self.rect.move_ip(0, -self.PIXELS_PER_FRAME)
            elif self.direction == self.DOWN:
                self.rect.move_ip(0, self.PIXELS_PER_FRAME)
            elif self.direction == self.LEFT:
                self.rect.move_ip(-self.PIXELS_PER_FRAME, 0)
            elif self.direction == self.RIGHT:
                self.rect.move_ip(self.PIXELS_PER_FRAME, 0)
            
            #Sprawdz czy animacje sie juz zakonczyla, jesli tak to odnotuj to
            if self.animation_it == self.FRAMES_PER_MOVE:
                self.animation_it = 0
                self.isMoving = 0
                
    def move(self, direction):
        if not self.isMoving:
            #Jezeli nie jestesmy w trakcie animacji to zainicjuj nowa
            self.direction = direction
            self.isMoving = True
            
            if self.direction == self.UP:
                self.image = self.image1
            elif self.direction == self.DOWN:
                self.image = self.image2
            elif self.direction == self.LEFT:
                self.image = self.image3
            elif self.direction == self.RIGHT:
                self.image = self.image4    
                
    
    def moveBack(self):
        #Cofnij ruch i zatrzymaj animacje
        if self.direction == self.UP:
            self.rect.move_ip(0, self.PIXELS_PER_FRAME)
        elif self.direction == self.DOWN:
            self.rect.move_ip(0, -self.PIXELS_PER_FRAME)
        elif self.direction == self.LEFT:
            self.rect.move_ip(self.PIXELS_PER_FRAME, 0)
        elif self.direction == self.RIGHT:
            self.rect.move_ip(-self.PIXELS_PER_FRAME, 0)
        
        self.isMoving = False
        self.animation_it = 0
        
class Bullet(MovingObject):
    
    def __init__(self, centerPoint, images, tileSize, framesPerMove, direction = 1, moveLength = 0): 
        MovingObject.__init__(self, centerPoint, images, tileSize, framesPerMove, direction, moveLength)
        
        #Chce zeby prostokat pocisku byl wiekszy niz jego zdjecie (ma niszczyc sciane na pelnej szerokosci)
        size = max(self.rect.width, self.rect.height)
        center = self.rect.center
        self.rect.height = size
        self.rect.width = size
        self.rect.center = center
        
        #Wczytaj i odtworz dzwiek wystrzalu:
        sound = pygame.mixer.Sound('sounds/shoot.wav')
        sound.play()
        

class Tank(MovingObject):
    
    def __init__(self, centerPoint, images, creatingImages, bigBumImages, tileSize, framesPerMove, bulletSpeed = 0, hp = 1, direction = 1):
        MovingObject.__init__(self, centerPoint, images, tileSize, framesPerMove, direction = 1)
        
        self.isDead = False
        self.framesToCreate = 30
        self.lastShoot = 10000
        self.lastDirectionChange = 10000
        self.creatingImages = creatingImages
        self.bigBumImages = bigBumImages
        self.creatingImagesIt = 0
        self.hp = hp
        if bulletSpeed:
            self.bulletSpeed = bulletSpeed
        else:
            self.bulletSpeed = tileSize/4
    
    def update(self):
        if self.framesToCreate > 1:
            self.framesToCreate -= 1
            self.creatingImagesIt = (self.creatingImagesIt + 1) % 4
            self.image = self.creatingImages[self.creatingImagesIt]
        elif self.framesToCreate == 1:
            self.framesToCreate -= 1
            self.image = self.image1
        else:
            MovingObject.update(self)
            self.lastShoot += 1
            self.lastDirectionChange += 1
    
    #Wykonuje ruch testowy, trzeba go potem cofnac!
    def testMove(self, direction):
        self.direction = direction
        if direction == self.UP:
            self.rect.move_ip(0, -self.PIXELS_PER_FRAME)
        elif direction == self.DOWN:
            self.rect.move_ip(0, self.PIXELS_PER_FRAME)
        elif direction == self.LEFT:
            self.rect.move_ip(-self.PIXELS_PER_FRAME, 0)
        elif direction == self.RIGHT:
            self.rect.move_ip(self.PIXELS_PER_FRAME, 0)
            
    def move(self, direction):
        if not self.framesToCreate:
            MovingObject.move(self,direction)
            
    def createBigBum(self):
        sound = pygame.mixer.Sound('sounds/explosion.wav')
        sound.play()
        big_bum = AnimatedGameObject(self.rect.center, self.bigBumImages, 4)
        return big_bum
    
    def respawn(self, point):
        self.isMoving = False
        self.rect.center = point
        self.framesToCreate = 30
         
    def destroy():
        self.isDead = True
        
        
    
