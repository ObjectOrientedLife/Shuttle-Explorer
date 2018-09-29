# -*- coding: cp949 -*-
# Galaxy Explorer
# By Park Changhwi

#������ �ö󰥼��� �༺�� ��Ʋ�� �۾�����
#ȸ���Ҽ��� ���ᰡ ��´�
#���� �༺�� ������ ������
#���� �༺�� ������ ���� ����
#������ ������ ���� ����
#���ᰡ ���ϸ� ���� ��
#�Ķ� �༺������ ���� ���� ����

import pygame, random, time, math, sys, copy
from pygame.locals import *

try:
    import android
except ImportError:
    android = None
 
class Planet(): # �༺ Ŭ����
    def __init__(self, level):
        self.level = level
        self.numberOfPlanets = int(self.level**0.4) * 4 # ��ü ������ ������ �༺�� ����
        self.size = int(120 / int(self.level ** 0.4)) + 10
        
        self.planetList = [] # ������ �༺���� ������ ��� ����Ʈ
        self.count = 0
        self.blueplanet = pygame.transform.scale(BLUEPLANET, (self.size, self.size))
        self.planetXList = list(range(0, int(SCREENSIZE[0] / self.size)))
        self.planetYList = list(range(0, int(SCREENSIZE[1] / self.size)))

        self.planetXList.remove(int(SCREENSIZE[0] / (self.size * 2)))
        self.planetXList.remove(int(SCREENSIZE[1] / (self.size * 2)))
        self.planetXList.remove(int(1 + SCREENSIZE[0] / (self.size * 2)))
        self.planetXList.remove(int(1 + SCREENSIZE[1] / (self.size * 2)))

        while self.count < self.numberOfPlanets:
            self.x = random.choice(self.planetXList)
            self.y = random.choice(self.planetYList)
            
            self.planetXList.remove(self.x)
            self.planetYList.remove(self.y)
            planetDict = {'type': random.choice([BLUEPLANET, BLACKPLANET, REDPLANET]),
                          'x': self.size * self.x,
                          'y': self.size * self.y,
                          'size': self.size - random.randint(0, self.size / 2),
                          'degree': random.randint(0, 360)} # ������ �༺�� ������ ��� ��ųʸ�
            self.planetList.append(planetDict)
            self.count += 1


    def update(self, draw = True): # ������ ������Ʈ��
        self.planetObjList = []
        self.draw = draw
        for p in self.planetList:
            self.randomFact = random.randint(0, 10)
            self.planetObj = pygame.transform.scale(p['type'], (p['size'], p['size']))
            self.planetObj = pygame.transform.rotate(self.planetObj, p['degree'])
            self.planetRect = self.planetObj.get_rect(center = (p['x'], p['y']))
            if draw == True:
                DISPLAYSURF.blit(self.planetObj, self.planetRect)
                DISPLAYSURF.blit(self.blueplanet, (SCREENSIZE[0] / 2 - self.size / 2, SCREENSIZE[1] / 2 - self.size / 2))
            self.planetObjList.append((self.planetRect, p['x'], p['y'], p['type'], p['size']))
        return self.planetObjList

    def flag(self, flagData):
        self.flagData = flagData
        for f in self.flagData:
            flagrect = FLAG.get_rect(center = (f[0], f[1]))
            DISPLAYSURF.blit(FLAG, flagrect)
        self.defaultFlagRect = FLAG.get_rect(center = (SCREENSIZE[0] / 2, SCREENSIZE[1] / 2))
        DISPLAYSURF.blit(FLAG, self.defaultFlagRect)
    

class Shuttle(): # ��Ʋ Ŭ����
    def update(self, x, y, angle, launchMode): #angle�� ��Ʋ�� ����
        self.shuttleX = x
        self.shuttleY = y
        self.angle = angle
        self.launchMode = launchMode
        self.distance = 5 # ��Ʋ�� �ӵ��� ����
        if self.launchMode == False:
            self.rotatedShuttle = pygame.transform.rotate(SHUTTLE, self.angle)
        else:
            self.rotatedShuttle = pygame.transform.rotate(LAUNCHEDSHUTTLE, self.angle)
            
    def launch(self, launchFact, count): # ��Ʋ �߻�
        self.launchFact = launchFact
        self.count = count
        if self.launchFact == True:
            self.shuttleX -= self.count**1.6 * self.distance * math.sin(math.radians(self.angle))
            self.shuttleY -= self.count**1.6 * self.distance * math.cos(math.radians(self.angle))

    def draw(self, launchMode, count):
        self.launchMode = launchMode
        self.count = count
        self.launch(self.launchMode, self.count)
        self.shuttleRect = self.rotatedShuttle.get_rect(center = (self.shuttleX, self.shuttleY))
        DISPLAYSURF.blit(self.rotatedShuttle, self.shuttleRect)

    def returnRect(self):
        return self.shuttleRect


class Display():
    def level(self, currentLevel):
        self.currentLevel = currentLevel
        self.levelText = BASICFONT.render('Level: %s'%self.currentLevel, True, WHITE, BACKGROUNDCOLOR)
        DISPLAYSURF.blit(self.levelText, (400, 600))

    def score(self, currentScore):
        self.currentScore = currentScore
        self.scoreText = BASICFONT.render('Score: %s'%self.currentScore, True, WHITE, BACKGROUNDCOLOR)
        DISPLAYSURF.blit(self.scoreText, (400, 640))

    def fuel(self, currentFuel):
        self.currentFuel = currentFuel
        self.gaugeAngle = - 0.9 * self.currentFuel + 45
        self.gauge1Rect = GAUGE1.get_rect(center = (640, 620))
        self.rotatedGauge2 = pygame.transform.rotate(GAUGE2, self.gaugeAngle)
        self.gauge2Rect = self.rotatedGauge2.get_rect(center = (640, 620))
        self.fuelText = BASICFONT.render('FUEL GAUGE', True, WHITE, BACKGROUNDCOLOR)
        DISPLAYSURF.blit(GAUGE1, self.gauge1Rect)
        DISPLAYSURF.blit(self.rotatedGauge2, self.gauge2Rect)
        DISPLAYSURF.blit(self.fuelText, (573, 655))

        
class  Control():
    def __init__(self, level, score, fuel):
        self.done = False

        self.currentLevel = level
        self.currentScore = score
        self.currentFuel = fuel
        
        self.planet = Planet(self.currentLevel)
        self.shuttle = Shuttle()
        self.display = Display()

        self.x = SCREENSIZE[0] / 2
        self.y = SCREENSIZE[1] / 2

        self.angle = 0 # �ʱ� ��Ʋ ����
        self.degree = 3# �����Ӵ� ������ ��Ʋ�� ����
        self.speed = 5 # �����Ӵ� ������ ��Ʋ�� �Ÿ�
        self.count = 0 # ��Ʋ�� ������ Ƚ��
        self.launchMode = False # ��Ʋ �߻� ����

        self.flagData = []

        self.fuelMode = 'blue'

        #self.startMenu()

        self.planetData = self.planet.update(False)
        while not self.done:
            self.mainloop()


    def mainloop(self): # ���� ����
        self.FPSCLOCK = pygame.time.Clock()
        while True:
            DISPLAYSURF.fill(BLACK)
            self.planet.update() # �༺�� ����
            self.planet.flag(self.flagData)
            self.shuttle.update(self.x, self.y, self.angle, self.launchMode) # ��Ʋ�� ������ �°� ����
            self.shuttle.draw(self.launchMode , self.count) # �߻� ��忡 ���� �߻�
 
            self.event() # �̺�Ʈ ó�� �Լ�
            self.angle += self.degree # ��Ʋ ���� ����
            
            if self.launchMode == True:
                self.count += 1 # ��Ʋ�� ������ �Ÿ� ����
                self.checkForCollide()

            if self.fuelMode == 'blue':
                self.currentFuel -= 0
            elif self.fuelMode == 'black':
                self.currentFuel -= 0.2
            elif self.fuelMode == 'red':
                self.currentFuel -= 0.35
            elif self.fuelMode == 'launch':
                self.currentFuel -= 0.45
            
            self.display.level(self.currentLevel)
            self.display.score(self.currentScore)
            self.display.fuel(self.currentFuel)

            pygame.display.update()
            self.FPSCLOCK.tick(FPS)
            
    def event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                self.degree = 0 # ��Ʋ�� ���̻� ȸ������ ����
                self.launchMode = True # �߻� ���θ� True�� ��ȯ
                self.fuelMode = 'launch'
            if android:
                if android.check_pause():
                    android.wait_for_resume()


    def checkForCollide(self): # �浹 ����
        for p in self.planetData:
            if p[0].colliderect(self.shuttle.returnRect()):
                self.launchMode = False # �߻� ��带 False�� ��ȯ
                self.x = p[1] #��Ʋ�� x�� �༺�� x�� ��ü
                self.y = p[2] #��Ʋ�� y�� �༺�� y�� ��ü
                
                if p[3] == BLUEPLANET:
                    self.currentScore += p[4] / 9
                    self.fuelMode = 'blue'
                elif p[3] == BLACKPLANET:
                    self.currentScore += p[4] / 6
                    self.currentFuel += p[4] / 2 
                    self.fuelMode = 'black'
                elif p[3] == REDPLANET:
                    self.currentScore += p[4] / 3
                    self.fuelMode = 'red'
                
                self.degree = 3
                self.count = 0
                self.flagData.append((p[1], p[2]))
                self.planetData.remove(p)

        if  not DISPLAYRECT.colliderect(self.shuttle.returnRect()):
            self.done = True
            self.currentLevel += 1
            self.fuelMode = 'blue'
            run = Control(self.currentLevel, self.currentScore, self.currentFuel )

def main():
    global BASICFONT, FPS, SCREENSIZE, BACKGROUNDCOLOR, BLACK, WHITE, DISPLAYSURF, DISPLAYRECT, BLUEPLANET, BLACKPLANET, REDPLANET, SHUTTLE, LAUNCHEDSHUTTLE, FLAG, GAUGE1, GAUGE2
    pygame.init()
    pygame.font.init()
    
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
 

    BASICFONT = pygame.font.SysFont("comicsansms", 20)

    FPS = 30
    SCREENSIZE = (1280, 720)
    BACKGROUNDCOLOR = (0, 0, 0)
    
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    pygame.display.set_caption("galaxyExplorer")
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    DISPLAYRECT = DISPLAYSURF.get_rect()
    
    BLUEPLANET = pygame.image.load("blueplanet.png")
    BLACKPLANET = pygame.image.load("blackplanet.png")
    REDPLANET = pygame.image.load("redplanet.png")
    SHUTTLE = pygame.image.load("shuttle.png")
    LAUNCHEDSHUTTLE = pygame.image.load("launchedshuttle.png")
    FLAG = pygame.image.load("flag.png")
    FLAG = pygame.transform.scale(FLAG, (30, 30))

    SHUTTLE = pygame.transform.scale(SHUTTLE, (50, 75))
    LAUNCHEDSHUTTLE = pygame.transform.scale(LAUNCHEDSHUTTLE, (55, 78))

    GAUGE1 = pygame.image.load("gauge1.png")
    GAUGE2 = pygame.image.load("gauge2.png")
    GAUGE1 = pygame.transform.scale(GAUGE1, (150, 150))
    GAUGE2 = pygame.transform.scale(GAUGE2, (150, 150))
    
    run = Control(1, 0, 100) #�ʱ� ���� 1, �ʱ� ���� 0, �ʱ� ���� 100

if __name__ == "__main__":
    main()

        
    

    
            
            
            
        
        
    
        
        
        
    
