#   PyGame Pac-Man Like Game "Peter the Eater"      #
#   Jeffrey Dickson                                 #
#   Sep 2022                                        #

#Initialize Modules
import pygame, sys, random, time, peterConfig

#Define some variables
scale = peterConfig.screenScale
screenWidth = int(600 + (scale * 200)) #=1200
screenHeight = int(500 + (scale * 100)) #=600
cellX = 29
cellY = 32
cellPx = int(15 + (scale * 3)) #int(screenHeight/cellY) 
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
clockTickSet = int(10 + (scale * 30))
paused = False
doorsOpen = False
lives = 3
waitTime = 1
scatterTime = 1000
enemyTargX = 0
enemyTargY = 0
trackList = ["sound/Leap.wav","sound/Turns.wav","sound/nightshift.wav","sound/Kalimba.wav","sound/Spooky.wav"]
#Good: "sound/Leap.wav","sound/Turns.wav","sound/nightshift.wav","sound/Kalimba.wav","sound/Spooky.wav"
cutSceneLock = False

#Initialize some title changes
pygame.display.set_caption('Pickaxe Pete')
gameIcon = pygame.image.load('img/pick.png')
pygame.display.set_icon(gameIcon)

#Define some levels as strings
level1Template =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level1Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level1Template += "xwp...........ww...........pw"
level1Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level1Template += "xw.wxxw.wxxxw.ww.wxxxw.wxxw.w"
level1Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level1Template += "xw..........................w"
level1Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level1Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level1Template += "xw......ww....ww....ww......w"
level1Template += "xwwwwww.wwwwwxwwxwwwww.wwwwww"
level1Template += "xxxxxxw.wwwwwxwwxwwwww.wxxxxx"
level1Template += "xxxxxxw.wwxxxxxxxxxxww.wxxxxx"
level1Template += "xxxxxxw.wwxwwwwwwwwxww.wxxxxx"
level1Template += "xxxxxxw.wwxwwwwwwwwxww.wxxxxx"
level1Template += "xxxxxxw.xxxxxxxexxxxxx.wxxxxx"
level1Template += "xxxxxxwgwwwwwwwwwwwwwwgwxxxxx"
level1Template += "xxxxxxw.wwwwwwwwwwwwww.wxxxxx"
level1Template += "xxxxxxw.ww..........ww.wxxxxx"
level1Template += "xxxxxxw.ww.wwwwwwww.ww.wxxxxx"
level1Template += "xwwwwww.ww.wwwwwwww.ww.wwwwww"
level1Template += "xw............ww............w"
level1Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level1Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level1Template += "xw...ww.......xx.......ww...w"
level1Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level1Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level1Template += "xw......ww....ww....ww......w"
level1Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level1Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level1Template += "xwp...........ss...........pw"
level1Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

level2Template = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level2Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level2Template += "xws...p...wwwwwwwwww...p...sw"
level2Template += "xw.wwwwww.....ww.....wwwwww.w"
level2Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level2Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level2Template += "xw......ww..........ww......w"
level2Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level2Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level2Template += "xw............ww............w"
level2Template += "xwwwwww.wwwwwgwwgwwwww.wwwwww"
level2Template += "xxxxwww.wwwwwxwwxwwwww.wwwxxx"
level2Template += "xxxxw...ww..........ww...wxxx"
level2Template += "xxxxw.wwww.wwwggwww.wwww.wxxx"
level2Template += "xxxxw.wxxw.wxxxxxxw.wxxw.wxxx"
level2Template += "xxxxw.wxxw.wxxxxxxw.wxxw.wxxx"
level2Template += "xxxxw.wxxw.wexxxxew.wxxw.wxxx"
level2Template += "xwwww.wwww.wwwggwww.wwww.wwww"
level2Template += "xw......ww..........ww......w"
level2Template += "xw.wwww.wwwwwxwwxwwwww.wwww.w"
level2Template += "xw.wwww.wwwwwgwwgwwwww.wwww.w"
level2Template += "xw..........................w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw...ww.ww....xx....ww.ww...w"
level2Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level2Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level2Template += "xw............ww............w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xws.......p........p.......sw"
level2Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

level3Template = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level3Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level3Template += "xw...wwwwwwwwwwwwwwwwwwww...w"
level3Template += "xw.w.........wwww.........w.w"
level3Template += "xw.w.wwwwwww.wwww.wwwwwww.w.w"
level3Template += "xw.w.wwwwwww.wwww.wwwwwww.w.w"
level3Template += "xw.w.p..ww..........ww..p.w.w"
level3Template += "xw.w.ww.ww.ww.ww.ww.ww.ww.w.w"
level3Template += "xw.w.ww.ww.ww.ww.ww.ww.ww.w.w"
level3Template += "xw...ww.......ww.......ww...w"
level3Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level3Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level3Template += "xwww.ww.ww..........ww.ww.www"
level3Template += "xwww.ww.wwwwwwxxwwwwww.ww.www"
level3Template += "xwww.ww.wwwwwwxxwwwwww.ww.www"
level3Template += "xwww.ww.ww..........ww.ww.www"
level3Template += "xwww.ww....wwwwwwww....ww.www"
level3Template += "xwww.ww.wwwwwwwwwwwwww.ww.www"
level3Template += "xwww.ww.wwwwwwwwwwwwww.ww.www"
level3Template += "xwww.ww.wwwww....wwwww.ww.www"
level3Template += "xwww.ww.......ww.......ww.www"
level3Template += "xwwwswwswwwwwwwwwwwwwwswwswww"
level3Template += "xwww.ww.gxxxxxeexxxxxg.ww.www"
level3Template += "xwww.ww.wwwwwwwwwwwwww.ww.www"
level3Template += "xwww.ww.......xx.......ww.www"
level3Template += "xwww.wwwww.wwwwwwww.wwwww.www"
level3Template += "xwww.wwwww.wwwwwwww.wwwww.www"
level3Template += "xw...p..................p...w"
level3Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level3Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level3Template += "xw............ww............w"
level3Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

level4Template = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level4Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level4Template += "xw...p..p..p......p..p..p...w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw...p..p..p..ww..p..p..p...w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw...p..p..p..ww..p..p..p...w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw.ww.ww.ww.wwwwww.ww.ww.ww.w"
level4Template += "xw..........................w"
level4Template += "xwgwwwwwwwwwwwwwwwwwwwwwwwwgw"
level4Template += "xw..........................w"
level4Template += "xw.wwww.wwwwwwwwwwwwww.wwww.w"
level4Template += "xw.wwww.wwwwwwwwwwwwww.wwww.w"
level4Template += "xw......exxxxxeexxxxxe......w"
level4Template += "xwgwwwwwwwwwwwwwwwwwwwwwwwwgw"
level4Template += "xw.......swwwwwwwwwws.......w"
level4Template += "xw.wwwwww.wwwwwwwwww.wwwwww.w"
level4Template += "xw.wwwwww.wwwwwwwwww.wwwwww.w"
level4Template += "xw.wwwwww.....ww.....wwwwww.w"
level4Template += "xw........www.ww.www........w"
level4Template += "xwww.wwwwwwww.ww.wwwwwwww.www"
level4Template += "xwww.wwwwwwww.xx.wwwwwwww.wxx"
level4Template += "xxxw......www.ww.www......wxx"
level4Template += "xxxw.wwww.www.ww.www.wwww.wxx"
level4Template += "xxxw.wwww.www.ww.www.wwww.wxx"
level4Template += "xxxw.wwww.www.ww.www.wwww.wxx"
level4Template += "xxxw.wwww.www.ww.www.wwww.wxx"
level4Template += "xxxw..........ww..........wxx"
level4Template += "xxxwwwwwwwwwwwwwwwwwwwwwwwwxx"

levelList = [level1Template, level2Template, level3Template, level4Template]

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
            pygame.mixer.Sound.play(self.getSound)
            addScore(100)

class Man(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, color):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
    def update(self):
        self.rect.topleft = [manX, manY]
    def setLeft(self):
        #self.image.fill((255,255,255))
        print("Left")
    def setRight(self):
        #self.image.fill((0,255,0))
        print("Right")
    def setUp(self):
        #self.image.fill((0,0,255))
        print("Up")
    def setDown(self):
        #self.image.fill((255,0,0))
        print("Down")

class Enemy(pygame.sprite.Sprite): #Enemy(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
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
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, enemyGroup, False)
        for block in blockingHit:
            removeLife(1)
        
        if int(self.ePosX % cellPx) == 0 and int(self.ePosY % cellPx) == 0:
            #Code to find direction should go here
            self.eGridX = (self.ePosX)/cellPx
            self.eGridY = (self.ePosY)/cellPx
            
            if self.ePosX > enemyTargX and levelCollideCheck(self.eGridX, self.eGridY, 0) == False and self.eDirection != 1:
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
    print(doorsOpen)
    #pygame.sprite.Group.empty(switchGroup)
    #pygame.sprite.Group.empty(doorGroup)
def cutSceneLockSet(boolIn):
    global cutSceneLock
    cutSceneLock = boolIn

def removeLife(amount):
    global lives
    lives -= amount
    setupLevel(levelList[level])
    setupEnemy(levelList[level])
    setupDoors(levelList[level])
    setupSwitch(levelList[level])
    setManLocation(manStartX, manStartY)
    setWaitTime(1)

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
    waitTime = amount
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


#set up enemy group
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
man = Man(cellPx, cellPx, manStartX, manStartY, (255, 212, 123))
manGroup = pygame.sprite.Group()
manGroup.add(man)

font = pygame.font.SysFont(None, 35 + scale*3)

while True:
    ####    Main Menu    ####
    mainMenu = True
    background = pygame.image.load("img/Mountain.png")
    DEFAULT_BACKGROUND_SIZE = (screenWidth, screenHeight)
    background = pygame.transform.scale(background, DEFAULT_BACKGROUND_SIZE)
    pygame.mouse.set_visible(False)
    while mainMenu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                mainMenu = False
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
    setupLevel(levelList[0])
    setupFood(levelList[0])
    setupEnemy(levelList[0])
    setupDoors(levelList[0])
    setupSwitch(levelList[0])
    setupPick(levelList[0])

    #Primary Game Loop
    while lives > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    man.setLeft()
                    setDir = 0
                elif event.key == pygame.K_RIGHT:
                    man.setRight()
                    setDir = 1
                elif event.key == pygame.K_UP:
                    man.setUp()
                    setDir = 2
                elif event.key == pygame.K_DOWN:
                    man.setDown()
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
                    setupSwitch(levelList[level])
                    setupDoors(levelList[level])
                    setupPick(levelList[level])
                    manX = manStartX
                    manY = manStartY
                    print("Next Level")
        ManGridCheckpoint(manX, manY) #Primary Movement for player character
        
        
        #Toggle Scatter Mode for enemies
        if scatterTime > 300:
            setEnemyTarg(manX, manY)
        elif scatterTime <= 300:
            setEnemyTarg(random.randint(0, cellX) * cellPx,random.randint(0, cellY) * cellPx)
            if scatterTime <= 0:
                scatterTime = 1000
        print(scatterTime)
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

        #Check for level completion
        if (currentFood <= 0):
            addLevel(1)
            setupLevel(levelList[level])
            setupFood(levelList[level])
            setupEnemy(levelList[level])
            setupDoors(levelList[level])
            setupSwitch(levelList[level])
            setupPick(levelList[level])
            manX = manStartX
            manY = manStartY
            
        #Draw Background
        pygame.display.flip()
        screen.fill((14,14,14))
        #screen.blit(background, (0,0))
        wallGroup.draw(screen)
        foodGroup.draw(screen)
        switchGroup.draw(screen)
        doorGroup.draw(screen)
        pickGroup.draw(screen)
        #Draw Enemies
        enemyGroup.draw(screen)
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
            doorGroup.update()
            switchGroup.update()
            pickGroup.update()
            scatterTime -= 1
        #Wait if needed
        time.sleep(waitTime)
        setWaitTime(0)
        clock.tick(clockTickSet)