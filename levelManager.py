import pygame
from pygame.locals import *
from Wall import Wall
from SpriteSheetLoader import ImageLoader
from GameObject import GameObject, AnimatedGameObject
import MovingObjects
import random

class LevelManager:
    
    def __init__(self, levelMatrix, tileSize, imageTileSize, x_offset, y_offset):
        self.LEVEL_MATRIX = levelMatrix
        
        #stale dekodujace wartosci w macierzy na odpowiednie obiekty gry
        self.WALL = 1
        self.UPPER_HALF_WALL = 1.2
        self.LOWER_HALF_WALL = 1.4
        self.STONE_WALL = 2
        self.GRASS = 3
        self.PLAYER = 4
        self.BASE = 5
        self.WATER = 6
        self.FLOOR = 7
        self.FRAME = 9
        
        self.isKeyUpDown = False
        self.isKeyDownDown = False
        self.isKeyLeftDown = False
        self.isKeyRightDown = False
        
        #Ile czasu temu gracz oddal ostatni strzal, potrzebne by nie strzelac za szybko
        self.playerLastShoot = 100000
        self.lastEnemyCreated = 100000
        self.enemiesLeft = 20
        self.livesLeft = 2
        self.levelWon = False
        self.gameOver = False
        self.currentRespawn = 0
        
        #Prawdopodobienstwa pojawienia sie typow czolgu
        self.p1 = 0.33
        self.p2 = 0.33
        
        #Zmienne zwiazane z odleglosciami do rysowania na planszy
        self.tileSize = tileSize
        self.imageTileSize = imageTileSize
        self.offset = tileSize/2
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.multiplier = self.tileSize/self.imageTileSize
        
        #Zaladuj obrazki ze spriteSheet do zmiennych
        self.loadImages()
        
        #Utworz grupy obiektow
        self.wallSprites = pygame.sprite.Group()
        self.stoneWallSprites = pygame.sprite.Group()
        self.grassSprites = pygame.sprite.Group()
        self.frameSprites = pygame.sprite.Group()
        self.waterSprites = pygame.sprite.Group()
        self.floorSprites = pygame.sprite.Group()
        self.playerBulletSprites = pygame.sprite.Group()
        self.enemyBulletSprites = pygame.sprite.Group()
        self.BUMS = pygame.sprite.Group()
        self.BIG_BUMS = pygame.sprite.Group()
        self.enemySprites = pygame.sprite.Group()
        
        #Na podstawie mapy poziomu dodaj odpowiednie obiekty do grup
        self.loadLevel(levelMatrix)
        
        #zaladuj panel wyswietlajacy informacje o stanie rozgrywki
        self.loadInfoPanel()
                    
    def loadImages(self):
        imageTileSize = self.imageTileSize
        self.loader = ImageLoader(multiplier = self.multiplier)        
        self.WALL_IMAGE = self.loader.getImage((imageTileSize*16, 0, imageTileSize, imageTileSize))
        self.STONE_WALL_IMAGE = self.loader.getImage((imageTileSize*16, imageTileSize, imageTileSize, imageTileSize))
        self.GRASS_IMAGE = self.loader.getImage((imageTileSize*17, 2*imageTileSize, imageTileSize, imageTileSize), -1)
        self.WATER_IMAGE = self.loader.getImage((imageTileSize*16, 3*imageTileSize, imageTileSize, imageTileSize))
        self.FLOOR_IMAGE = self.loader.getImage((imageTileSize*18, 2*imageTileSize, imageTileSize, imageTileSize))
        self.FRAME_IMAGE = self.loader.getImage((imageTileSize*23+1, 0, imageTileSize, imageTileSize))
        self.PLAYER_IMAGE_UP = self.loader.getImage((0, 0, imageTileSize, imageTileSize), -1)
        self.PLAYER_IMAGE_DOWN = self.loader.getImage((imageTileSize*5, 0, imageTileSize, imageTileSize), -1)
        self.PLAYER_IMAGE_LEFT = self.loader.getImage((imageTileSize*3, 0, imageTileSize, imageTileSize), -1)
        self.PLAYER_IMAGE_RIGHT = self.loader.getImage((imageTileSize*7, 0, imageTileSize, imageTileSize), -1)
        self.CREATING_TANK1 = self.loader.getImage((imageTileSize*16, imageTileSize*6, imageTileSize, imageTileSize),-1)
        self.CREATING_TANK2 = self.loader.getImage((imageTileSize*17, imageTileSize*6, imageTileSize, imageTileSize),-1)
        self.CREATING_TANK3 = self.loader.getImage((imageTileSize*18, imageTileSize*6, imageTileSize, imageTileSize),-1)
        self.CREATING_TANK4 = self.loader.getImage((imageTileSize*19, imageTileSize*6, imageTileSize, imageTileSize),-1)
        self.CREATING_TANK_IMAGES = (self.CREATING_TANK1, self.CREATING_TANK2, self.CREATING_TANK3, self.CREATING_TANK4)
        self.ENEMY_IMAGE_UP_1 = self.loader.getImage((imageTileSize*8, imageTileSize, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_DOWN_1 = self.loader.getImage((imageTileSize*12, imageTileSize, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_LEFT_1 = self.loader.getImage((imageTileSize*10, imageTileSize, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_RIGHT_1 = self.loader.getImage((imageTileSize*14, imageTileSize, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_UP_2 = self.loader.getImage((imageTileSize*8, imageTileSize*7, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_DOWN_2 = self.loader.getImage((imageTileSize*12, imageTileSize*7, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_LEFT_2 = self.loader.getImage((imageTileSize*10, imageTileSize*7, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_RIGHT_2 = self.loader.getImage((imageTileSize*14, imageTileSize*7, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_UP_3 = self.loader.getImage((imageTileSize*8, imageTileSize*5, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_DOWN_3 = self.loader.getImage((imageTileSize*12, imageTileSize*5, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_LEFT_3 = self.loader.getImage((imageTileSize*10, imageTileSize*5, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGE_RIGHT_3 = self.loader.getImage((imageTileSize*14, imageTileSize*5, imageTileSize, imageTileSize),-1)
        self.ENEMY_IMAGES_1 = (self.ENEMY_IMAGE_UP_1, self.ENEMY_IMAGE_DOWN_1, self.ENEMY_IMAGE_LEFT_1, self.ENEMY_IMAGE_RIGHT_1)
        self.ENEMY_IMAGES_2 = (self.ENEMY_IMAGE_UP_2, self.ENEMY_IMAGE_DOWN_2, self.ENEMY_IMAGE_LEFT_2, self.ENEMY_IMAGE_RIGHT_2)
        self.ENEMY_IMAGES_3 = (self.ENEMY_IMAGE_UP_3, self.ENEMY_IMAGE_DOWN_3, self.ENEMY_IMAGE_LEFT_3, self.ENEMY_IMAGE_RIGHT_3)
        self.BASE_IMAGE = self.loader.getImage((imageTileSize*19, 2*imageTileSize, imageTileSize, imageTileSize))
        self.DAMAGED_BASE_IMAGE = self.loader.getImage((imageTileSize*20, 2*imageTileSize, imageTileSize, imageTileSize))
        self.BULLET_IMAGE_UP = self.loader.getImage((imageTileSize*20, 6*imageTileSize, imageTileSize/2, imageTileSize),-1)
        self.BULLET_IMAGE_LEFT = self.loader.getImage((imageTileSize*20.5, 6*imageTileSize, imageTileSize/2, imageTileSize),-1)
        self.BULLET_IMAGE_DOWN = self.loader.getImage((imageTileSize*21, 6*imageTileSize, imageTileSize/2, imageTileSize),-1)
        self.BULLET_IMAGE_RIGHT = self.loader.getImage((imageTileSize*21.5, 6*imageTileSize, imageTileSize/2, imageTileSize),-1)
        self.BUM_IMAGE1 = self.loader.getImage((imageTileSize*16, 8*imageTileSize, imageTileSize, imageTileSize), -1)
        self.BUM_IMAGE2 = self.loader.getImage((imageTileSize*17, 8*imageTileSize, imageTileSize, imageTileSize), -1)
        self.BUM_IMAGE3 = self.loader.getImage((imageTileSize*18, 8*imageTileSize, imageTileSize, imageTileSize), -1)
        self.BUM_IMAGES = (self.BUM_IMAGE1, self.BUM_IMAGE2, self.BUM_IMAGE3)
        self.BIG_BUM_IMAGE1 = self.loader.getImage((imageTileSize*19, 8*imageTileSize, imageTileSize*2, imageTileSize*2), -1)
        self.BIG_BUM_IMAGE2 = self.loader.getImage((imageTileSize*21+1, 8*imageTileSize, imageTileSize*2, imageTileSize*2), -1)
        self.BIG_BUM_IMAGES = (self.BIG_BUM_IMAGE1, self.BIG_BUM_IMAGE2)
        
    def loadLevel(self, levelMatrix):
        offset = self.offset
        tileSize = self.tileSize
        
        for y in range(len(levelMatrix)):
            for x in range(len(levelMatrix[y])):
                if levelMatrix[y][x] == self.WALL:
                    wall = Wall((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.WALL_IMAGE)
                    for corner in wall.getWallCorners():
                        self.wallSprites.add(corner)
                elif levelMatrix[y][x] == self.STONE_WALL:
                    stoneWall = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.STONE_WALL_IMAGE)
                    self.stoneWallSprites.add(stoneWall)
                elif levelMatrix[y][x] == self.GRASS:
                    grass = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.GRASS_IMAGE)
                    self.grassSprites.add(grass)
                elif levelMatrix[y][x] == self.WATER:
                    water = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.WATER_IMAGE)
                    self.waterSprites.add(water)
                elif levelMatrix[y][x] == self.FLOOR:
                    floor = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.FLOOR_IMAGE)
                    self.floorSprites.add(floor)
                elif levelMatrix[y][x] == self.FRAME:
                    frame = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.FRAME_IMAGE)
                    self.frameSprites.add(frame)
                elif levelMatrix[y][x] == self.PLAYER:
                    images = (self.PLAYER_IMAGE_UP, self.PLAYER_IMAGE_DOWN, self.PLAYER_IMAGE_LEFT, self.PLAYER_IMAGE_RIGHT)
                    self.playerRespPoint = (self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset)
                    self.player = MovingObjects.Tank(self.playerRespPoint, images, self.CREATING_TANK_IMAGES, self.BIG_BUM_IMAGES, tileSize, 4)
                    self.playerSprite = pygame.sprite.RenderPlain(self.player)
                elif levelMatrix[y][x] == self.BASE:
                    self.base = GameObject((self.x_offset + x*tileSize+offset, self.y_offset + y*tileSize+offset), self.BASE_IMAGE)
                    self.baseSprite = pygame.sprite.RenderPlain(self.base)
    
    def loadInfoPanel(self):
        #Wczytuje dane do wyswietlania informacji na panelu bocznym
        imageTileSize = self.imageTileSize
        self.IP_IMAGE = self.loader.getImage((imageTileSize*23.5, 8.5*imageTileSize, imageTileSize, imageTileSize/2), -1)
        self.IP_IMAGE2 = self.loader.getImage((imageTileSize*23.5, 9*imageTileSize, imageTileSize/2, imageTileSize/2), -1)
        self.TANK_IMAGE = self.loader.getImage((imageTileSize*20, 12*imageTileSize, imageTileSize/2, imageTileSize/2), -1)
        self.NUMBER_0 = self.loader.getImage((self.imageTileSize*20.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_1 = self.loader.getImage((self.imageTileSize*21, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        self.NUMBER_2 = self.loader.getImage((self.imageTileSize*21.5, 11.5*self.imageTileSize, self.imageTileSize/2, self.imageTileSize/2))
        
        self.enemiesLeftSprites = []
        for i in range(10):
            center = (self.x_offset + (len(self.LEVEL_MATRIX[0])-2) * self.tileSize + 1.5*self.offset, self.y_offset + 4*self.tileSize + i*self.tileSize/2)
            enemySprite = pygame.sprite.RenderPlain(GameObject(center, self.TANK_IMAGE))
            self.enemiesLeftSprites.append(enemySprite)
            
            center = (self.x_offset + (len(self.LEVEL_MATRIX[0])-2) * self.tileSize + 1.5*self.offset + self.tileSize/2, self.y_offset + 4*self.tileSize + i*self.tileSize/2)
            enemySprite = pygame.sprite.RenderPlain(GameObject(center, self.TANK_IMAGE))
            self.enemiesLeftSprites.append(enemySprite)
        
        self.playerInfoSprites = []
        center = (self.x_offset + (len(self.LEVEL_MATRIX[0])-2) * self.tileSize + 1.5*self.offset, self.y_offset + 4*self.tileSize + 15*self.tileSize/2)
        self.playerInfoSprites.append(pygame.sprite.RenderPlain(GameObject(center, self.IP_IMAGE)))
        center = (center[0] - self.tileSize/4, center[1] + self.tileSize/2)
        self.playerInfoSprites.append(pygame.sprite.RenderPlain(GameObject(center, self.IP_IMAGE2)))
        center = (center[0] + self.tileSize/2, center[1])
        self.livesLeftObject = GameObject(center, self.NUMBER_2)
        self.playerInfoSprites.append(pygame.sprite.RenderPlain(self.livesLeftObject))
    
    def startMove(self, key):
        if key == K_UP:
            self.isKeyUpDown = True
        if key == K_DOWN:
            self.isKeyDownDown = True
        if key == K_LEFT:
            self.isKeyLeftDown = True
        if key == K_RIGHT:
            self.isKeyRightDown = True
            
    def stopMove(self, key):
        if key == K_UP:
            self.isKeyUpDown = False
        if key == K_DOWN:
            self.isKeyDownDown = False
        if key == K_LEFT:
            self.isKeyLeftDown = False
        if key == K_RIGHT:
            self.isKeyRightDown = False
            
    def movePlayer(self):
        if self.isKeyUpDown:
            self.player.move(self.player.UP)
            return
        if self.isKeyDownDown:
            self.player.move(self.player.DOWN)
            return
        if self.isKeyLeftDown:
            self.player.move(self.player.LEFT)
            return
        if self.isKeyRightDown:
            self.player.move(self.player.RIGHT)
            return
        
    def moveEnemy(self, enemy):
        #Jezeli czolg jest w trakcie animacji to nic nie robimy
        if enemy.isMoving:
            return
        
        #Aktualny kierunek ruchu
        curDirection = enemy.direction
        
        #Najpierw sprawdzamy wszystkie mozliwe kierunki, ktore nie spowoduja kolizji
        directionsPossible = []
        allDirections = [1, 2, 3, 4]
        
        for direction in allDirections:
            enemy.testMove(direction)
            wallColisions = pygame.sprite.spritecollide(enemy, self.wallSprites, False)
            stoneWallColisions = pygame.sprite.spritecollide(enemy, self.stoneWallSprites, False)
            frameCollisions = pygame.sprite.spritecollide(enemy, self.frameSprites, False)
            waterColisions = pygame.sprite.spritecollide(enemy, self.waterSprites, False)
            baseColisions = pygame.sprite.spritecollide(enemy, self.baseSprite, False)
            if not len(wallColisions) + len(stoneWallColisions) + len(frameCollisions) + len(baseColisions) + len(waterColisions):
                directionsPossible.append(direction)
            enemy.moveBack()
            
        #Jezeli ostatnio zmienialismy kierunek to nie zmieniajmy go ponownie, pod warunkiem ze mamy takie wyjscie (tzn nie jestesmy w "slepej uliczce")
        if enemy.lastDirectionChange < 30 and curDirection in directionsPossible:
            enemy.move(curDirection)
            return
        
        #Wyznaczam kierunek przeciwny do kierunku ruchu
        if curDirection == enemy.UP:
            oppositeDir = enemy.DOWN
        elif curDirection == enemy.DOWN:
            oppositeDir = enemy.UP
        elif curDirection == enemy.LEFT:
            oppositeDir = enemy.RIGHT
        elif curDirection == enemy.RIGHT:
            oppositeDir = enemy.LEFT
            
        #Jezeli czolg na otwartej przestrzeni to niech nie zmienia bez sensu kierunku
        if len(directionsPossible) == 4:
            enemy.move(curDirection)
            return
         
        #Nie cofamy sie w tunelach
        if oppositeDir in directionsPossible and curDirection in directionsPossible and len(directionsPossible) == 2:
            directionsPossible.remove(oppositeDir)
        
        #Teraz juz losujemy kierunek w taki sposob by p-stwo cofniecia sie bylo rowne 0,02 (nie chcemy tego robic zbyt czesto)
        #oraz p-stwo pozostalych mozliwych ruchow po rowno.
        random.seed()
        
        nDirections = len(directionsPossible)
        
        direction = random.randint(0, nDirections-1)
            
        enemy.move(directionsPossible[direction])
        
        enemy.lastDirectionChange = 0
    
    def update(self):
        #Sprawdz czy mozna dodac wroga na plansze
        if self.lastEnemyCreated > 60 and len(self.enemySprites.sprites()) < 4 and len(self.enemiesLeftSprites):
            self.lastEnemyCreated = 0
            x = random.random()
            
            if x < self.p1:
                enemy = MovingObjects.Tank((self.x_offset + self.tileSize*(1+6*self.currentRespawn) + self.offset, self.y_offset + self.tileSize + self.offset),     self.ENEMY_IMAGES_1, self.CREATING_TANK_IMAGES, self.BIG_BUM_IMAGES, self.tileSize, 4)
            elif x < self.p1 + self.p2:
                enemy = MovingObjects.Tank((self.x_offset + self.tileSize*(1+6*self.currentRespawn) + self.offset, self.y_offset + self.tileSize + self.offset),     self.ENEMY_IMAGES_2, self.CREATING_TANK_IMAGES, self.BIG_BUM_IMAGES, self.tileSize, 4, hp=2)
            else:
                enemy = MovingObjects.Tank((self.x_offset + self.tileSize*(1+6*self.currentRespawn) + self.offset, self.y_offset + self.tileSize + self.offset),     self.ENEMY_IMAGES_3, self.CREATING_TANK_IMAGES, self.BIG_BUM_IMAGES, self.tileSize, 2, hp=2, bulletSpeed = self.tileSize/2)
                
            self.currentRespawn = (self.currentRespawn + 1) % 3
            self.enemySprites.add(enemy)
            
            self.enemiesLeftSprites.pop()
                   
        #Kontynuuj zaczety ruch (jesli jest zaczety) gracza i wrogow
        self.player.update()
        for enemy in self.enemySprites.sprites():
            enemy.update()
            
        #Strzaly wrogow
        for enemy in self.enemySprites.sprites():
            if enemy.lastShoot >= 30 and not enemy.framesToCreate:
                x = random.random()
                #Jesli uplynal odpowiedni czas to strzel z prawdopodobienstem 0.05
                if x < 0.05:
                    enemy.lastShoot = 0
                    images = self.BULLET_IMAGE_UP, self.BULLET_IMAGE_DOWN, self.BULLET_IMAGE_LEFT, self.BULLET_IMAGE_RIGHT
                    bullet = MovingObjects.Bullet(enemy.rect.center, images, self.tileSize, 1, enemy.direction, enemy.bulletSpeed)
                    bullet.move(enemy.direction)
                    self.enemyBulletSprites.add(bullet)
                    
        
        #Porusz gracza jesli trzeba
        self.movePlayer()
        
        #Porusz wrogow jesli trzeba
        for enemy in self.enemySprites.sprites():
            self.moveEnemy(enemy)
        
        #Uaktualnij odpowiedni liczniki
        self.playerLastShoot += 1
        self.lastEnemyCreated += 1
        
        #Porusz pociski wrogow
        for bullet in self.enemyBulletSprites.sprites():
            bullet.update()
            bullet.move(bullet.direction)
            
        #Porusz pociski gracza
        for bullet in self.playerBulletSprites.sprites():
            bullet.update()
            bullet.move(bullet.direction)
        
        #Sprawdz kolizje pociskow wrogow z scianami, ramka, czolgami itd.
        self.handleEnemiesBulletsColisions()
        
        #Sprawdz kolizje pociskow gracza.
        self.handlePlayerBulletsColisions()
        
        #Uaktualnij animacje wybuchow
        for BUM in self.BUMS:
            isEnded = BUM.update()
            if isEnded:
                self.BUMS.remove(BUM)
        
        for BUM in self.BIG_BUMS:
            isEnded = BUM.update()
            if isEnded:
                self.BIG_BUMS.remove(BUM)

        #Sprawdz kolizje gracza, cofnij ruch jesli doszlo do kolizji
        wallColisions = pygame.sprite.spritecollide(self.player, self.wallSprites, False)
        stoneWallColisions = pygame.sprite.spritecollide(self.player, self.stoneWallSprites, False)
        frameCollisions = pygame.sprite.spritecollide(self.player, self.frameSprites, False)
        baseColisions = pygame.sprite.spritecollide(self.player, self.baseSprite, False)
        waterColisions = pygame.sprite.spritecollide(self.player, self.waterSprites, False)
        
        if len(wallColisions) + len(frameCollisions) + len(stoneWallColisions) + len(baseColisions) + len(waterColisions) > 0:
            self.player.moveBack()
        
        #Sprawdz czy gra zostala wygrana
        if not len(self.enemiesLeftSprites) + len(self.enemySprites):
            self.levelWon = True
            
    def handlePlayerBulletsColisions(self):
        for bullet in self.playerBulletSprites.sprites():
            
            wallColisions = pygame.sprite.spritecollide(bullet, self.wallSprites, True)
            stoneWallColisions = pygame.sprite.spritecollide(bullet, self.stoneWallSprites, False)
            frameColisions = pygame.sprite.spritecollide(bullet, self.frameSprites, False)
            enemyColisions = pygame.sprite.spritecollide(bullet, self.enemySprites, False)
            
            #Jesli doszlo do kolizji do stworz WYBUCH i usun pocisk
            if len(wallColisions) + len(stoneWallColisions) + len(frameColisions) + len(enemyColisions): 
                BUM = AnimatedGameObject(bullet.rect.center, self.BUM_IMAGES, 3)
                self.BUMS.add(BUM)
                self.playerBulletSprites.remove(bullet)
            
            #Dla wszystkich czolgow trafionych pociskiem: zmniejsz hp,  wygeneruj duzy wybuch jesli hp spadlo do zera
            for tank in enemyColisions:
                tank.hp -= 1
                if tank.hp == 0:
                    self.enemySprites.remove(tank)
                    bigBum = tank.createBigBum()
                    self.BIG_BUMS.add(bigBum)
                    self.enemiesLeft -= 1

                
            self.enemiesLeft -= len(enemyColisions)
    
    def handleEnemiesBulletsColisions(self):
        for bullet in self.enemyBulletSprites.sprites():
            
            wallColisions = pygame.sprite.spritecollide(bullet, self.wallSprites, True)
            stoneWallColisions = pygame.sprite.spritecollide(bullet, self.stoneWallSprites, False)
            frameColisions = pygame.sprite.spritecollide(bullet, self.frameSprites, False)
            playerColisions = pygame.sprite.spritecollide(bullet, self.playerSprite, False)
            baseColisions = pygame.sprite.spritecollide(bullet, self.baseSprite, False)
            
            if len(playerColisions):
                bigBum = self.player.createBigBum()
                self.BIG_BUMS.add(bigBum)
                
                if self.livesLeft:
                    self.player.respawn(self.playerRespPoint)
                    self.livesLeft -= 1
                    if self.livesLeft == 1:
                        self.livesLeftObject.changeImage(self.NUMBER_1)
                    elif self.livesLeft == 0:
                        self.livesLeftObject.changeImage(self.NUMBER_0)
                else:
                    self.gameOver = True
            
            #Jesli doszlo do kolizji do stworz WYBUCH i usun pocisk
            if len(wallColisions) + len(stoneWallColisions) + len(frameColisions) + len(playerColisions) + len(baseColisions): 
                BUM = AnimatedGameObject(bullet.rect.center, self.BUM_IMAGES, 3)
                self.BUMS.add(BUM)
                self.enemyBulletSprites.remove(bullet)
                
            if len(baseColisions):
                self.base.changeImage(self.DAMAGED_BASE_IMAGE)
                self.gameOver = True
        
    def shootRequest(self):
        if self.player.lastShoot >= 10 and not self.player.framesToCreate:
            self.player.lastShoot = 0
            images = self.BULLET_IMAGE_UP, self.BULLET_IMAGE_DOWN, self.BULLET_IMAGE_LEFT, self.BULLET_IMAGE_RIGHT
            bullet = MovingObjects.Bullet(self.player.rect.center, images, self.tileSize, 1, self.player.direction, self.tileSize/4)
            bullet.move(self.player.direction)
            self.playerBulletSprites.add(bullet)
                        
    def render(self, screen):
        self.frameSprites.draw(screen)
        self.wallSprites.draw(screen)
        self.stoneWallSprites.draw(screen)
        self.waterSprites.draw(screen)
        self.floorSprites.draw(screen)
        self.playerSprite.draw(screen)
        self.enemySprites.draw(screen)
        self.baseSprite.draw(screen)
        self.playerBulletSprites.draw(screen)
        self.enemyBulletSprites.draw(screen)
        self.grassSprites.draw(screen)
        self.BUMS.draw(screen)
        self.BIG_BUMS.draw(screen)
        for e in self.enemiesLeftSprites:
            e.draw(screen)
        for i in self.playerInfoSprites:
            i.draw(screen)

        
                    
