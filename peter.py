#   PyGame Pac-Man Like Game "Peter the Eater"      #
#   Jeffrey Dickson                                 #
#   Sep 2022                                        #

#Initialize Modules
import pygame, sys, random, time, peterConfig
from PeterTemplates import *

#Define some variables
scale = peterConfig.screenScale
cellX = 29
cellY = 32
cellPx = int(15 + (scale * 3)) #int(screenHeight/cellY) 
screenWidth = int((cellPx * cellX) + (cellPx * 15)) #=1200
screenHeight = int((cellPx * cellY) + cellPx) #=600
peterDir = 0 # 0 left 1 right 2 up 3 down 
setDir = 0
manStartX = cellPx * 14
manStartY = cellPx * 24
manX = manStartX
manY = manStartY
bCanContinue = True
score = 0
currentFood = 0
level = 0
clockTickSet = int(20 + (scale * 6))
paused = False
doorsOpen = False
lives = 3
waitTime = 1
scatterTime = 1000
enemyTargX = 0
enemyTargY = 0
trackList = ["sound/Leap.wav","sound/Turns.wav","sound/nightshift.wav","sound/Kalimba.wav","sound/Spooky.wav"]
#Good: "sound/Leap.wav","sound/Turns.wav","sound/nightshift.wav","sound/Kalimba.wav","sound/Spooky.wav"
cutSceneLock = True
nVolume = 0.5

print(str(screenWidth) + " x " + str(screenHeight))
#Initialize some title changes
pygame.display.set_caption('Pickaxe Pete / F3~F4 Scale game / F5~F6 Sound level / F11 Pause')
gameIcon = pygame.image.load('img/pick.png')
pygame.display.set_icon(gameIcon)

#Classes used
class Wall(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    def update(self, color):
        self.image.fill(color)

class Food(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("img/pill.png")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.getSound = pygame.mixer.Sound("sound/get.wav")
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, foodGroup, True)
        for block in blockingHit:
            self.getSound.set_volume(nVolume)
            pygame.mixer.Sound.play(self.getSound)
            addScore(10)
            removeFood(1)

class Pick(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("img/pick.png")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.getSound = pygame.mixer.Sound("sound/pickPickup.wav")
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, pickGroup, True)
        for block in blockingHit:
            self.getSound.set_volume(nVolume)
            pygame.mixer.Sound.play(self.getSound)
            addScore(100)

#### Man Sprite and sprite sheet ####
manSprites = ["img/peter.png", "img/peter1.png", "img/peter2.png", "img/peter3.png", "img/peter4.png", "img/peter5.png"]
crabSprites = ["img/crab1.png", "img/crab2.png"]
class Man(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image = pygame.image.load("img/peter.png")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        #self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    def update(self):
        self.rect.topleft = [manX , manY] #- int((cellPx * 1.5)/4)
    def animUpdate(self, direction, frame):
        if direction == 1 or direction == 3:
            self.image = pygame.image.load(manSprites[frame % 3])
        else:
            self.image = pygame.image.load(manSprites[(frame % 3) + 3])
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx)) 

class Enemy(pygame.sprite.Sprite): #Enemy(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image = pygame.image.load("img/crab1.png")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.eDirection = 0
        self.eI = 0
        self.ePosX = pos_x
        self.ePosY = pos_y
        self.eGridX = 0
        self.eGridY = 0
        self.getSound = pygame.mixer.Sound("sound/hit.wav")
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, enemyGroup, False)
        for block in blockingHit: #Collisions with player cause death to player
            self.getSound.set_volume(nVolume)
            pygame.mixer.Sound.play(self.getSound)
            removeLife(1)
        
        if int(self.ePosX % cellPx) == 0 and int(self.ePosY % cellPx) == 0: #When aligned with a grid location
            #Code to find direction should go here
            self.eGridX = (self.ePosX)/cellPx
            self.eGridY = (self.ePosY)/cellPx
            
            if self.ePosX > enemyTargX and levelCollideCheck(self.eGridX, self.eGridY, 0) == False and self.eDirection != 1: #Set direction towards the target
                self.eDirection = 0
            elif self.ePosX < enemyTargX and levelCollideCheck(self.eGridX, self.eGridY, 1) == False and self.eDirection != 0:
                self.eDirection = 1
            elif self.ePosY > enemyTargY and levelCollideCheck(self.eGridX, self.eGridY, 2) == False and self.eDirection != 3:
                self.eDirection = 2
            elif self.ePosY < enemyTargY and levelCollideCheck(self.eGridX, self.eGridY, 3) == False and self.eDirection != 2:
                self.eDirection = 3
            else:
                while levelCollideCheck(self.eGridX, self.eGridY, self.eDirection) == True:
                    self.eDirection = random.randint(0,3)
            
            
        match self.eDirection:
            case 0: #Left
                self.ePosX = self.ePosX - 3
            case 1: #Right
                self.ePosX = self.ePosX + 3
            case 2: #Up
                self.ePosY = self.ePosY - 3
            case 3: #Down
                self.ePosY = self.ePosY + 3
            case 4:
                print("Can't move!")
        self.rect.topleft = [self.ePosX, self.ePosY]
    def animUpdateEnemy(self, frame):
        self.image = pygame.image.load(crabSprites[frame % 2])
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx)) 

class NagaEnemy(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.eDirection = 0
        self.eI = 0
        self.ePosX = pos_x
        self.ePosY = pos_y
        self.eGridX = 0
        self.eGridY = 0
        self.nagID = pos_x + pos_y
        self.getSound = pygame.mixer.Sound("sound/hit.wav")
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, nagaGroup, False)
        for block in blockingHit: #Collisions with player cause death to player
            self.getSound.set_volume(nVolume)
            pygame.mixer.Sound.play(self.getSound)
            removeLife(1)
        
        if int(self.ePosX % cellPx) == 0 and int(self.ePosY % cellPx) == 0: #When aligned with a grid location
            #Code to find direction should go here
            self.eGridX = (self.ePosX)/cellPx
            self.eGridY = (self.ePosY)/cellPx
            
            if self.ePosX > enemyTargX and levelCollideCheck(self.eGridX, self.eGridY, 0) == False and self.eDirection != 1: #Set direction towards the target
                self.eDirection = 0
            elif self.ePosX < enemyTargX and levelCollideCheck(self.eGridX, self.eGridY, 1) == False and self.eDirection != 0:
                self.eDirection = 1
            elif self.ePosY > enemyTargY and levelCollideCheck(self.eGridX, self.eGridY, 2) == False and self.eDirection != 3:
                self.eDirection = 2
            elif self.ePosY < enemyTargY and levelCollideCheck(self.eGridX, self.eGridY, 3) == False and self.eDirection != 2:
                self.eDirection = 3
            else:
                while levelCollideCheck(self.eGridX, self.eGridY, self.eDirection) == True:
                    self.eDirection = random.randint(0,3)
            
            #Draw "rays"
            
            setupTemp(0, 0, True, 0) #Clear old ones
            nagX = self.eGridX #Check these X grid positions
            nagB = True #Boolean
            nagCW = False #Check Wall
            for nagXP in range(20): #check 10 squares away from ourselves in both directions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~You are here!
                if nagB is True:
                    nagX = nagX + nagXP
                    nagB = False
                else:
                    nagX = nagX - nagXP
                    nagB = True
                
                if levelList[level][int(self.eGridY * cellX  + nagX)] != "w" and nagCW == False:
                    setupTemp(nagX, self.eGridY, False, self.nagID)
                else:
                    nagCW = True
                
            nagY = self.eGridY #Check these X grid positions
            nagB = True #Boolean
            nagCW = False #Check Wall
            for nagYP in range(20): 
                if nagB is True:
                    nagY = nagY + nagYP
                    nagB = False
                else:
                    nagY = nagY - nagYP
                    nagB = True
                
                if levelList[level][clamp(int(nagY * cellX  + self.eGridX), 0, cellX * cellY - 1)] != "w" and nagCW == False:
                    setupTemp(self.eGridX, nagY, False, self.nagID)
                else:
                    nagCW = True   
        match self.eDirection: #The naga moves a 1px per update as opposed to the canary which moves at the same speed as the player
            case 0: #Left
                self.ePosX = self.ePosX - 1
            case 1: #Right
                self.ePosX = self.ePosX + 1
            case 2: #Up
                self.ePosY = self.ePosY - 1
            case 3: #Down
                self.ePosY = self.ePosY + 1
            case 4:
                print("Can't move!")
        self.rect.topleft = [self.ePosX, self.ePosY]
    def fireNagas(self, ID):
        if ID == self.nagID:
            print("fire thing at guy")
                
#TEMPORARY hit detectors
class tempSprite(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, ID):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill((100,100,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.tempID = ID
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, nagaIndicatorGroup, False)
        for block in blockingHit: #Collisions with player cause death to player
            print("OBLITERATE HIM..." + str(self.tempID))
    

#TEMPORARY hit detector group
nagaIndicatorGroup = pygame.sprite.Group()
def setupTemp(xLoc, yLoc, empty, ID):
    global nagaIndicatorGroup
    if empty == True:
        pygame.sprite.Group.empty(nagaIndicatorGroup)
    else:
        newTemp = tempSprite(cellPx, cellPx, xLoc * cellPx, yLoc * cellPx, ID)
        nagaIndicatorGroup.add(newTemp)

class Door(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("img/Door.png")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.xLoc = pos_x
        self.yLoc = pos_y
    def update(self):
        if doorsOpen == True:
            self.image = pygame.image.load("img/DoorOpen.png")
            self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.xLoc, self.yLoc]

class Switch(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load("img/Switch.png")
        self.getSound = pygame.mixer.Sound("sound/switch.wav")
        self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.xLoc = pos_x
        self.yLoc = pos_y
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, switchGroup, False)
        for block in blockingHit:
            if doorsOpen == False:
                self.getSound.set_volume(nVolume)
                pygame.mixer.Sound.play(self.getSound)
            openDoors(True)
        if doorsOpen == True:
            self.image = pygame.image.load("img/SwitchFlip.png")
            self.image = pygame.transform.scale(self.image, (cellPx, cellPx))
            self.rect = self.image.get_rect()
            self.rect.topleft = [self.xLoc, self.yLoc]

def levelCollideCheck(currentX, currentY, askDirection): #takes Coords in grid space not pixel space
    currentX = int(currentX)
    currentY = int(currentY)
    match askDirection: #Check if we can change our existing movement
        case 0: #Left
            if levelList[level][currentY * cellX  + clamp(currentX - 1, 0 , cellX)] == "w":
                return True
            elif doorsOpen == False and levelList[level][currentY * cellX  + clamp(currentX - 1, 0 , cellX)] == "g":
                return True
        case 1: #Right
            if levelList[level][currentY * cellX  + clamp(currentX + 1, 0 , cellX)] == "w":
                return True
            elif doorsOpen == False and levelList[level][currentY * cellX  + clamp(currentX + 1, 0 , cellX)] == "g":
                return True
        case 2: #Up
            if levelList[level][clamp((currentY - 1) * cellX, 0, cellY*cellX) + currentX] == "w":
                return True
            elif doorsOpen == False and levelList[level][clamp((currentY - 1) * cellX, 0, cellY*cellX) + currentX] == "g":
                return True
        case 3: #Down
            if levelList[level][ clamp((currentY + 1) * cellX, 0, cellY*cellX) + currentX ] == "w":
                return True
            elif doorsOpen == False and levelList[level][ clamp((currentY + 1) * cellX, 0, cellY*cellX) + currentX ] == "g":
                return True
    return False

#Functions used
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def ManGridCheckpoint(locX, locY): #location X and location Y of the player character
    #We are on the grid coords make x and y values in grid values not pixels
    gridX = int(locX/cellPx)
    gridY = int(locY/cellPx)
    global bCanContinue
    global peterDir
    global setDir
    bCanContinue = True
    
    if setDir == 0 and peterDir == 1:
        peterDir = setDir
    if setDir == 1 and peterDir == 0:
        peterDir = setDir
    if setDir == 2 and peterDir == 3:
        peterDir = setDir
    if setDir == 3 and peterDir == 2:
        peterDir = setDir
        
    if int(manX % cellPx) == 0 and int(manY % cellPx) == 0 : #Check if we align on the grid coords in pixels
        
        #First Check if we're on a food
        newFood.update()
        newSwitch.update()
        newPick.update()
        match setDir:#Check if we can change our existing movement
            case 0: #Left
                if levelCollideCheck(gridX, gridY, 0) == False:
                    peterDir = setDir
            case 1: #Right
                if levelCollideCheck(gridX, gridY, 1) == False:
                    peterDir = setDir
            case 2: #Up
                if levelCollideCheck(gridX, gridY, 2) == False:
                    peterDir = setDir
            case 3: #Down
                if levelCollideCheck(gridX, gridY, 3) == False :
                    peterDir = setDir
        
        match peterDir:#Check if we can change our existing movement
            case 0: #Left
                if levelCollideCheck(gridX, gridY, 0) == True:
                    bCanContinue = False
            case 1: #Right
                if levelCollideCheck(gridX, gridY, 1) == True:
                    bCanContinue = False
            case 2: #Up
                if levelCollideCheck(gridX, gridY, 2) == True:
                    bCanContinue = False
            case 3: #Down
                if levelCollideCheck(gridX, gridY, 3) == True:
                    bCanContinue = False

def addScore(amount):
    global score
    score += amount

def removeFood(amount):
    global currentFood
    currentFood -= amount
    
def addLevel(amount):
    global level
    level = (level + amount) % len(levelList)

def openDoors(boolIn):
    global doorsOpen
    doorsOpen = boolIn
    #print(doorsOpen)
    #pygame.sprite.Group.empty(switchGroup)
    #pygame.sprite.Group.empty(doorGroup)
def cutSceneLockSet(boolIn):
    global cutSceneLock
    cutSceneLock = boolIn

def removeLife(amount):
    global lives
    lives -= amount
    time.sleep(.5)
    setupLevel(levelList[level])
    setupEnemy(levelList[level])
    setupEnemyNaga(levelList[level])
    setupDoors(levelList[level])
    setupSwitch(levelList[level])
    setManLocation(manStartX, manStartY)

def resetLife(amount):
    global lives
    lives = amount

def setManLocation(pos_x, pos_y):
    global manX
    global manY
    manX = pos_x
    manY = pos_y

def setEnemyTarg(pos_x, pos_y):
    global enemyTargX
    global enemyTargY
    enemyTargX = pos_x
    enemyTargY = pos_y

def setWaitTime(amount):
    global waitTime
    waitTime = time.process_time() + amount

def setNewScale(amount):
    global scale
    global screenWidth
    global screenHeight
    global cellPx
    global manStartX
    global manStartY
    global manX
    global manY
    global screen
    global background
    scale += amount
    cellPx = int(15 + (scale * 3))
    screenWidth = int((cellPx * cellX) + (cellPx * 15)) #=1200
    screenHeight = int((cellPx * cellY) + cellPx) #=600
    manStartX = cellPx * 14
    manStartY = cellPx * 24
    manX = manStartX
    manY = manStartY
    DEFAULT_BACKGROUND_SIZE = (screenWidth, screenHeight)
    background = pygame.transform.scale(background, DEFAULT_BACKGROUND_SIZE)
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)

#General Setup and backdrop
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen.fill((14,14,14))

#set up background as group
wallGroup = pygame.sprite.Group()
def setupLevel(level):
    global wallGroup
    pygame.mixer.music.stop()
    pygame.mixer.music.load(trackList[random.randint(0,len(trackList) - 1)])
    pygame.mixer.music.play(-1)
    pygame.sprite.Group.empty(wallGroup)
    xP = 0
    yP = 0
    setColor = (255,255,255)
    wallColor = (random.randint(14,123),random.randint(14,123),random.randint(14,123))
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "w":
                setColor = (wallColor)
            else:
                setColor = (14,14,14)
            newWall = Wall(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
            wallGroup.add(newWall)

#Set up Doors
doorGroup = pygame.sprite.Group()
def setupDoors(level):
    global doorGroup
    global newDoor
    openDoors(False)
    pygame.sprite.Group.empty(doorGroup)
    xP=0
    yP=0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "g":
                newDoor = Door(cellPx, cellPx, xP * cellPx, yP * cellPx)
                doorGroup.add(newDoor)
                
#set up pellet group
foodGroup = pygame.sprite.Group()
def setupFood(level):
    global foodGroup
    global newFood
    pygame.sprite.Group.empty(foodGroup)
    xP = 0
    yP = 0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == ".":
                setColor = (123,123,123)
                newFood = Food(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
                foodGroup.add(newFood)
                removeFood(-1)

#Set up switches
switchGroup = pygame.sprite.Group()
def setupSwitch(level):
    global switchGroup
    global newSwitch
    pygame.sprite.Group.empty(switchGroup)
    xP=0
    yP=0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "s":
                newSwitch = Switch(cellPx, cellPx, xP * cellPx, yP * cellPx)
                switchGroup.add(newSwitch)


#set up canary enemy group
enemyGroup = pygame.sprite.Group()
def setupEnemy(level):
    global enemyGroup
    global newEnemy
    pygame.sprite.Group.empty(enemyGroup)
    xP = 0
    yP = 0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "e":
                setColor = (123,46,46)
                newEnemy = Enemy(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
                enemyGroup.add(newEnemy)

#set up naga enemy group
nagaGroup = pygame.sprite.Group()
def setupEnemyNaga(level):
    global nagaGroup
    global newNaga
    pygame.sprite.Group.empty(nagaGroup)
    xP = 0
    yP = 0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "n":
                setColor = (46,123,46)
                newNaga = NagaEnemy(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
                nagaGroup.add(newNaga)


#set up pellet group
pickGroup = pygame.sprite.Group()
def setupPick(level):
    global pickGroup
    global newPick
    pygame.sprite.Group.empty(pickGroup)
    xP = 0
    yP = 0
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "p":
                newPick = Pick(cellPx, cellPx, xP * cellPx, yP * cellPx)
                pickGroup.add(newPick)

#set up Peter group

manGroup = pygame.sprite.Group()


font = pygame.font.SysFont(None, 35 + scale*3)

background = pygame.image.load("img/Mountain.png")
DEFAULT_BACKGROUND_SIZE = (screenWidth, screenHeight)
background = pygame.transform.scale(background, DEFAULT_BACKGROUND_SIZE)

while True:
    ####    Main Menu    ####
    mainMenu = True
    pygame.mixer.music.set_volume(0.5)
    
    while mainMenu:
        pygame.mixer.music.stop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    mainMenu = False
                elif event.key == pygame.K_F3:
                    setNewScale(-1)
                elif event.key == pygame.K_F4:
                    setNewScale(1)
                elif event.key == pygame.K_ESCAPE:
                    exit()
        pygame.display.flip()
        screen.blit(background,(0,0))
        pygame.display.flip()
        clock.tick(10)
    
    ####    Reset Relevant Variables    ####
    mainMenu = True
    resetLife(3)
    removeFood(currentFood)
    addLevel(-level)
    addScore(-score)
    openDoors(False)
    
    ####    Primary Game    ####    
    #Prelevel Setup
    manX = manStartX
    manY = manStartY
    pygame.sprite.Group.empty(manGroup)
    man = Man(cellPx, cellPx, manStartX, manStartY, (255, 212, 123))
    manGroup.add(man)
    setupLevel(levelList[0])
    setupFood(levelList[0])
    setupEnemy(levelList[0])
    setupEnemyNaga(levelList[0])
    setupDoors(levelList[0])
    setupSwitch(levelList[0])
    setupPick(levelList[0])
    manAnimFrame = 0
    
    #optional wait between levels
    setWaitTime(.05)
    #Primary Game Loop
    while lives > 0:########################################################################################################################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    setDir = 0
                elif event.key == pygame.K_RIGHT:
                    setDir = 1
                elif event.key == pygame.K_UP:
                    setDir = 2
                elif event.key == pygame.K_DOWN:
                    setDir = 3
                elif event.key == pygame.K_F11:
                    if paused:
                        paused = False
                    else:
                        paused = True
                    print("Pause Game")
                elif event.key == pygame.K_F2:
                    addLevel(1)
                    removeFood(currentFood)
                    setupLevel(levelList[level])
                    setupFood(levelList[level])
                    setupEnemy(levelList[level])
                    setupEnemyNaga(levelList[level])
                    setupSwitch(levelList[level])
                    setupDoors(levelList[level])
                    setupPick(levelList[level])
                    manX = manStartX
                    manY = manStartY
                    cutSceneLockSet(True)
                    setWaitTime(.2)
                    print("Next Level")
                elif event.key == pygame.K_F5:
                    nVolume = clamp(nVolume - .1, 0 ,1)
                    pygame.mixer.music.set_volume(nVolume)
                elif event.key == pygame.K_F6:
                    nVolume = clamp(nVolume + .1, 0 ,1)
                    pygame.mixer.music.set_volume(nVolume)
                    
                elif event.key == pygame.K_ESCAPE:
                    lives = 0
                elif event.key == pygame.K_r:
                    setupTemp(0, 0, True, 0)
        ManGridCheckpoint(manX, manY) #Primary Movement for player character
        manAnimFrame += 1
        if manAnimFrame > 300000:
            manAnimFrame = 0
        
        
        #Toggle Scatter Mode for enemies
        if scatterTime > 300:
            setEnemyTarg(manX, manY)
        elif scatterTime <= 300:
            setEnemyTarg(random.randint(0, cellX) * cellPx,random.randint(0, cellY) * cellPx)
            if scatterTime <= 0:
                scatterTime = 1000
        if bCanContinue == True and not paused and not cutSceneLock:
            match peterDir:
                case 0: #Left
                    manX = manX - 3
                case 1: #Right
                    manX = manX + 3
                case 2: #Up
                    manY = manY - 3
                case 3: #Down
                    manY = manY + 3
            man.animUpdate(peterDir, manAnimFrame) #update animation frames
        #Draw Background
        pygame.display.flip()
        screen.fill((14,14,14))
        #screen.blit(background, (0,0))
        wallGroup.draw(screen)
        #Draw TEMPORARY sprites
        nagaIndicatorGroup.draw(screen)
        foodGroup.draw(screen)
        switchGroup.draw(screen)
        doorGroup.draw(screen)
        pickGroup.draw(screen)
        #Draw Enemies
        enemyGroup.draw(screen)
        nagaGroup.draw(screen)
        #Draw Peter
        manGroup.draw(screen)
        #Draw Score
        screenText = font.render("Score: " + str(score), True, (123,123,123))
        screen.blit(screenText, (screenWidth * .75, screenHeight * .05))
        screenText = font.render("Lives: " + str(lives), True, (123,123,123))
        screen.blit(screenText, (screenWidth * .75, screenHeight * .1))
        
        #Update
        if not paused and not cutSceneLock:
            man.update()
            enemyGroup.update()
            newEnemy.animUpdateEnemy(manAnimFrame)
            nagaGroup.update()
            doorGroup.update()
            switchGroup.update()
            pickGroup.update()
            nagaIndicatorGroup.update()
            
            scatterTime -= 1
        #Wait if needed
        ####            Game Loop Clock             ####
        
                #Check for level completion
        if (currentFood <= 0):
            addLevel(1)
            setupLevel(levelList[level])
            setupFood(levelList[level])
            setupEnemy(levelList[level])
            setupEnemyNaga(levelList[level])
            setupDoors(levelList[level])
            setupSwitch(levelList[level])
            setupPick(levelList[level])
            setupTemp(0, 0, True, 0)
            cutSceneLockSet(True)
            setWaitTime(.01)
            manX = manStartX
            manY = manStartY
            man.update()
        
        if time.process_time() > waitTime:
            cutSceneLockSet(False)
        clock.tick(clockTickSet)
    setWaitTime(1)
    cutSceneLockSet(True)