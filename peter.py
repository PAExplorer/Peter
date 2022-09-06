#   PyGame Pac-Man Like Game "Peter the Eater"      #
#   Jeffrey Dickson                                 #
#   Sep 2022                                        #

#Initialize Modules
import pygame, sys, random

#Define some variables
scale = 1
screenWidth = 1600/scale
screenHeight = 900/scale
cellX = 29
cellY = 32
cellPx = 27 / scale#int(screenHeight/cellY) 
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
clockTickSet = int(100 / scale)
paused = False

#Define some levels as strings
level1Template =  "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level1Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level1Template += "xw............ww............w"
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
level1Template += "xw..........................w"
level1Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

level2Template = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level2Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level2Template += "xw..........................w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw.wxxw.wxxxw.ww.wxxxw.wxxw.w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw..........................w"
level2Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level2Template += "xw.wwww.ww.wwwwwwww.ww.wwww.w"
level2Template += "xw......ww....ww....ww......w"
level2Template += "xwwwwww.wwwww.ww.wwwww.wwwwww"
level2Template += "xxxxxxw.wwwww.ww.wwwww.wxxxxx"
level2Template += "xxxxxxw.wwxxxxxxxxxxww.wxxxxx"
level2Template += "xxxxxxw.wwxwwwwwwwwxww.wxxxxx"
level2Template += "xxxxxxw.wwxwwwwwwwwxww.wxxxxx"
level2Template += "xxxxxxw.xxexxxxxxxxexx.wxxxxx"
level2Template += "xxxxxxwgwwwwwwwwwwwwwwgwxxxxx"
level2Template += "xxxxxxw.wwwwwwwwwwwwww.wxxxxx"
level2Template += "xxxxxxw.ww..........ww.wxxxxx"
level2Template += "xxxxxxw.ww.wwwwwwww.ww.wxxxxx"
level2Template += "xwwwwww.ww.wwwwwwww.ww.wwwwww"
level2Template += "xw............ww............w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw.wwww.wwwww.ww.wwwww.wwww.w"
level2Template += "xw...ww.......xx.......ww...w"
level2Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level2Template += "xwww.ww.ww.wwwwwwww.ww.ww.www"
level2Template += "xw......ww....ww....ww......w"
level2Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level2Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level2Template += "xw..........................w"
level2Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

level3Template = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
level3Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"
level3Template += "xw...wwwwwwwwwwwwwwwwwwww...w"
level3Template += "xw.w.........wwww.........w.w"
level3Template += "xw.w.wwwwwww.wwww.wwwwwww.w.w"
level3Template += "xw.w.wwwwwww.wwww.wwwwwww.w.w"
level3Template += "xw.w....ww..........ww....w.w"
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
level3Template += "xw..........................w"
level3Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level3Template += "xw.wwwwwwwwww.ww.wwwwwwwwww.w"
level3Template += "xw............ww............w"
level3Template += "xwwwwwwwwwwwwwwwwwwwwwwwwwwww"

levelList = [level1Template, level2Template, level3Template]

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
    def update(self):
        blockingHit = pygame.sprite.spritecollide(man, foodGroup, True)
        for block in blockingHit:
            addScore(10)
            removeFood(1)

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
        if int(self.ePosX % cellPx) == 0 and int(self.ePosY % cellPx) == 0:
            #Code to find direction should go here
            self.eGridX = (self.ePosX)/cellPx
            self.eGridY = (self.ePosY)/cellPx
            
            if self.ePosX > manX and levelCharCheck(self.eGridX, self.eGridY, 0, "w") == False and self.eDirection != 1:
                print("A")
                self.eDirection = 0
            elif self.ePosX < manX and levelCharCheck(self.eGridX, self.eGridY, 1, "w") == False and self.eDirection != 0:
                print("B")
                self.eDirection = 1
            elif self.ePosY > manY and levelCharCheck(self.eGridX, self.eGridY, 2, "w") == False and self.eDirection != 3:
                print("C")
                self.eDirection = 2
            elif self.ePosY < manY and levelCharCheck(self.eGridX, self.eGridY, 3, "w") == False and self.eDirection != 2:
                print("D")
                self.eDirection = 3
            else:
                while levelCharCheck(self.eGridX, self.eGridY, self.eDirection, "w") == True:
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

def levelCharCheck(currentX, currentY, askDirection, askChar): #takes Coords in grid space not pixel space
    currentX = int(currentX)
    currentY = int(currentY)
    match askDirection: #Check if we can change our existing movement
        case 0: #Left
            if levelList[level][currentY * cellX  + clamp(currentX - 1, 0 , cellX)] == askChar:
                return True
        case 1: #Right
            if levelList[level][currentY * cellX  + clamp(currentX + 1, 0 , cellX)] == askChar:
                return True
        case 2: #Up
            if levelList[level][clamp((currentY - 1) * cellX, 0, cellY*cellX) + currentX] == askChar:
                return True
        case 3: #Down
            if levelList[level][ clamp((currentY + 1) * cellX, 0, cellY*cellX) + currentX ] == askChar:
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
        newFood.update()
        match setDir:#Check if we can change our existing movement
            case 0: #Left
                if levelList[level][gridY * cellX  + clamp(gridX - 1, 0 , cellX)] != "w":
                    peterDir = setDir
            case 1: #Right
                if levelList[level][gridY * cellX  + clamp(gridX + 1, 0 , cellX)] != "w":
                    peterDir = setDir
            case 2: #Up
                if levelList[level][clamp((gridY - 1) * cellX, 0, cellY*cellX) + gridX] != "w":
                    peterDir = setDir
            case 3: #Down
                if levelList[level][ clamp((gridY + 1) * cellX, 0, cellY*cellX) + gridX ] != "w":
                    peterDir = setDir
        
        match peterDir:#Check if we can change our existing movement
            case 0: #Left
                if levelList[level][gridY * cellX  + clamp(gridX - 1, 0 , cellX)] == "w":
                    bCanContinue = False
            case 1: #Right
                if levelList[level][gridY * cellX  + clamp(gridX + 1, 0 , cellX)] == "w":
                    bCanContinue = False
            case 2: #Up
                if levelList[level][clamp((gridY - 1) * cellX, 0, cellY*cellX) + gridX] == "w":
                    bCanContinue = False
            case 3: #Down
                if levelList[level][ clamp((gridY + 1) * cellX, 0, cellY*cellX) + gridX ] == "w":
                    bCanContinue = False

def addScore(amount):
    global score
    score += amount

def removeFood(amount):
    global currentFood
    currentFood -= amount
    
def addLevel(amount):
    global level
    level += amount

#General Setup and backdrop
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
screen.fill((14,14,14))

#set up background as group
wallGroup = pygame.sprite.Group()
def setupLevel(level):
    global wallGroup
    pygame.sprite.Group.empty(wallGroup)
    xP = 0
    yP = 0
    setColor = (255,255,255)
    for xP in range(0, cellX):
        for yP in range(0, cellY):
            if level[(yP * cellX) + xP] == "w":
                setColor = (46,123,92)
            elif level[(yP * cellX) + xP] == "g":
                setColor = (46,123,46)
            else:
                setColor = (14,14,14)
            newWall = Wall(cellPx, cellPx, xP * cellPx, yP * cellPx, setColor)
            wallGroup.add(newWall)

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

#set up Peter group
man = Man(cellPx, cellPx, manStartX, manStartY, (255, 212, 123))
manGroup = pygame.sprite.Group()
manGroup.add(man)

font = pygame.font.SysFont(None, 44)


#Prelevel Setup
setupLevel(levelList[0])
setupFood(levelList[0])
setupEnemy(levelList[0])
#Primary Game Loop
while True:
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
    
    ManGridCheckpoint(manX, manY) #Primary Movement for player character
    
    if bCanContinue == True and not paused:
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
        n = level % len(levelList)
        setupLevel(levelList[n])
        setupFood(levelList[n])
        setupEnemy(levelList[n])
        manX = manStartX
        manY = manStartY
        
    #Draw Background
    pygame.display.flip()
    screen.fill((14,14,14))
    #screen.blit(background, (0,0))
    wallGroup.draw(screen)
    foodGroup.draw(screen)
    #Draw Enemies
    enemyGroup.draw(screen)
    #Draw Peter
    manGroup.draw(screen)
    #Draw Score
    scoreBoard = font.render("Score: " + str(score), True, (123,123,123))
    screen.blit(scoreBoard, (screenWidth * .55, screenHeight * .05))
    #Update
    if not paused:
        man.update()
        enemyGroup.update()
    clock.tick(clockTickSet)

