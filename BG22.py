from pygame import *
from math import *
from random import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~ Player ~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Player:
    def __init__(self):
        self.x = 0
        self.y = 22
        self.points = [[0,0], [20,20], [14,40], [16,30], [0,15], [-16,30], [-14,40], [-20, 20], [0,0]]

        self.aVelocity = 0
        self.dir = 0
        self.hp = 3
        self.shotCooldown = 0
        self.bombCooldown = 0
        self.velocity = 0


    def setPos(self, x,y):
        newP = []
        for i in self.points:
            newP.append([x + i[0] - self.x, y + i[1] - self.y])
        self.points = newP
        self.x = x
        self.y = y

    def accel(self, a):
        self.velocity += a
        if self.velocity > 3:
            self.velocity = 3
        if self.velocity < -3:
            self.velocity = -3

    def move(self):
        dy = self.velocity*cos(radians(self.dir))
        dx = self.velocity*sin(radians(self.dir))
        self.x += dx
        self.y += dy
        newP = []
        for i in self.points:
            newP.append([i[0] + dx, i[1] + dy])
        self.points = newP

        if self.velocity > 0:
            self.velocity -= 0.025
        if self.velocity < 0:
            self.velocity += 0.025

        if self.velocity < 0.001 and self.velocity > 0:
            self.velocity = 0
        if self.velocity > -0.001 and self.velocity < 0:
            self.velocity = 0

    def rota(self, angle):
        self.aVelocity += angle
        if self.aVelocity > 2:
            self.aVelocity = 2
        if self.aVelocity < -2:
            self.aVelocity = -2

    def rotate(self):
        newP = []
        for i in self.points:
            oX = i[0] - self.x
            oY = i[1] - self.y
            a = radians(self.aVelocity)
            newP.append([(oX * cos(a) + oY * sin(a)) + self.x, (-oX * sin(a) + oY * cos(a)) + self.y])
        self.dir += self.aVelocity
        self.points = newP

        if self.aVelocity > 0:
            self.aVelocity -= 0.05
        if self.aVelocity < 0:
            self.aVelocity += 0.05



    def draw(self, s):
        vert = [[ int(i[0]), int(i[1]) ] for i in self.points]
        draw.polygon(s, (255,255,255), vert, 3)

    def trans(self):
        if self.x > 1080:
            self.setPos(0, self.y)
        if self.x < 0:
            self.setPos(1080, self.y)
        if self.y > 720:
            self.setPos(self.x, 0)
        if self.y < 0:
            self.setPos(self.x, 720)



class Bullet:
    def __init__(self, x, y, ang, time):
        self.x = x
        self.y = y
        self.dir = float(ang)
        self.time = time


    def move(self):
        dx = self.time*cos(radians(self.dir+90))
        dy = self.time*sin(radians(self.dir+90))
        self.x -= dx
        self.y += dy
        self.time = max(2, self.time - 0.05)

    def draw(self, s):
        dx = cos(radians(self.dir+90))
        dy = sin(radians(self.dir+90))
        draw.circle(s, (255,255,0), [int(self.x), int(self.y)], 4)





class Square:           # A type of enemy
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hp = 10
        self.RhombusPoints = [[self.x+25,self.y],[self.x+50,self.y+25],[self.x+25,self.y+50],[self.x,self.y+25]]
        self.RectPoints = [[x,y],[x+50,y],[x+50,y+50],[x+50,y]]
        self.direction = 0

    def draw(self):
        #draw.rect(screen,(124,252,0),Rect(self.x,self.y,50,50),1)
        #pt1,pt2,pt3,pt4 = [self.x+25,self.y],[self.x+50,self.y+25],[self.x+25,self.y+50],[self.x,self.y+25]
        #draw.polygon(screen,(125,252,0),[pt1,pt2,pt3,pt4],1)
        draw.polygon(screen,(125,252,0),self.RectPoints,1)
        draw.polygon(screen,(125,252,0),self.RhombusPoints,1)


    def rotate (self):
        newRect = []
        newRhom = []
        direction += randint(0,20)
        for i in self.RhombusPoints:
            oX = i[0]-self.x
            oY = i[1]-self.y
            a = radians(diretion)
            newRhom.append([(oX * cos(radians(a)) + oY * sin(radians(a)) + self.x), (-oX * sin(radians(a)) + oY * cos(radians(a)) + self.y)])


        for i in self.RectPoints:
            oX = i[0]-self.x
            oY = i[1]-self.y
            a = radians(diretion)
            newRhom.append([(oX * cos(radians(a)) + oY * sin(radians(a)) + self.x), (-oX * sin(radians(a)) + oY * cos(radians(a)) + self.y)])
        self.RhombusPoints = newRhom
        self.RectPoints = newRect







    def move (self,PlrX,PlrY):
        if self.x>PlrX:
            self.x -= randint(0,2)
        elif self.x<PlrX:
            self.x += randint(0,2)

        if self.y>PlrY:
            self.y -= randint(0,2)
        elif self.y<PlrY:
            self.y += randint(0,2)



class Explosion:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.dir = randint(0,360)
        self.velocity = randint(3,5)
        self.col = col


    def move(self):
        dx = self.velocity*cos(radians(self.dir))
        dy = self.velocity*sin(radians(self.dir))
        self.x += dx
        self.y += dy
        self.velocity = max(1, self.velocity - 0.1)

    def draw(self, s):
        draw.line(s, self.col, (self.x, self.y), (self.x + 15*cos(radians(self.dir)), self.y + 15*sin(radians(self.dir))), 3)




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~ Game ~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
init()
mixer.init()
size=(1080, 720)
screen=display.set_mode(size)
display.set_caption("Bad Game 2")
labelFont = font.SysFont("Ailerons", 50)
hsFont = font.SysFont("Ailerons", 70)

def createScrollStars(maxStars,surface):
    'Creates the initial starfield in levels (2D)'
    stars=[]
    for i in range(maxStars):
        star=[randint(0,surface.get_width()-1),randint(0,surface.get_height()-1),randint(1,100)] #[x,y,speed]
        if star[2]<60: #60% chance to move 1 unit per frame
            star[2]=1
        elif star[2]<95: #35% chance to move 1.5 units per frame
            star[2]=1.5
        else:           #5% chance to move 2 units per frame
            star[2]=2
        stars.append(star)
    return stars

def moveDrawStars(stars,surface):
    'Updates the starfield in levels'
    for star in stars:
        star[1]+=star[2] #Add star speed to y coord (Only move downwards)

        #Reset stars if offscreen
        if star[1]>=720: #If the star goes offscreen, generate another one
            star[1]=0
            star[0]=randint(0,1080-1)
            star[2]=choice([1,1.5,2])

        #Set color depending on speed
        if star[2]==1:
          color=(100,100,100) #Stars moving slower are less visible
        elif star[2]==1.5:
          color=(150,150,150)
        elif star[2]==2:
          color=(200,200,200)

        draw.circle(surface,color,[int(star[0]),int(star[1])],int(star[2]))

scrollStarList=createScrollStars(250,screen)

def menu():
    running = True
    fps = time.Clock()
    beginCap = labelFont.render("Start Game", 1, (0,0,0))
    highCap = labelFont.render("High Scores", 1, (0,0,0))
    quitCap = labelFont.render("Quit", 1, (0,0,0))
    buttons = [Rect(290, y * 80 + 360, 500, 65) for y in range(3)]
    text = ["PLAY GAME", "HIGH SCORE", "QUIT"]

    maxSize = 200
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "QUIT"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.fill((0,0,0))
        moveDrawStars(scrollStarList, screen)
        for r, v in zip(buttons, text):
            draw.rect(screen, (255, 255, 255), r)
            screen.blit(beginCap, (390, 360))
            screen.blit(highCap, (370, 440))
            screen.blit(quitCap, (485, 520))
            if (r.collidepoint(mpos)):
                draw.rect(screen, (5, 100, 255), r, 3)
                if (mb[0] == 1):
                    screen.fill((0,0,0))
                    return v

        display.flip()



def game():
    running = True
    fps = time.Clock()
    plr = Player()
    plr.setPos(540, 360)
    plrBullets = []
    squareEnemy = []

    explosions = []

    for i in range(randint(0,15)):
        squareEnemy.append(Square(randint(0,1080),randint(0,720)))

    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return 'QUIT'

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        keys = key.get_pressed()

        screen.fill((255,255,255))
        draw.rect(screen, (0,0,0), [10,10,1060, 700])

        if keys[K_w]:
            plr.accel(0.10)
        if keys[K_s]:
            plr.accel(-0.10)
        if keys[K_a]:
            plr.rota(1)
        if keys[K_d]:
            plr.rota(-1)

        if keys[K_g]:
            col = choice([(255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0)])
            for i in range(25):
                explosions.append(Explosion(mx, my, col))



        if keys[K_SPACE] and plr.shotCooldown == 0:
            plrBullets.append(Bullet(plr.x, plr.y, plr.dir, 8))
            plr.shotCooldown = 25
        if keys[K_ESCAPE]:
            return 'menu'

        for b in plrBullets:
            if b.x > 1100 or b.x < -20 or b.y > 740 or b.y < -20:
                plrBullets.remove(b)
            else:
                b.move()
                b.draw(screen)


        for e in squareEnemy:
            e.draw()
            e.move(plr.x, plr.y)

        plr.move()
        plr.trans()
        plr.rotate()
        plr.draw(screen)

        if plr.shotCooldown > 0:
            plr.shotCooldown -= 1

        for e in explosions:
            e.move()
            if e.velocity < randint(1,2):
                explosions.remove(e)
            else:
                e.draw(screen)

        display.flip()

def readScore():
    file = open("score.txt")
    score = file.readlines()
    for i in range (3):
        score[i] = score[i].strip("\n")
    return score

def saveScore(highscore):
    scores = readScore()
    if highscore > scores[0]:
        scores[0] = str(highscore)
    #elif
    pass


def displayHS():
    screen.fill((0,0,0))
    scores = readScore()
    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "QUIT"


        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            return "menu"
        for i in range (3):
            screen.blit(hsFont.render(str((i + 1)) + ". " + scores[i],1,(255,255,255)), (250, 180 + 80 * i))
        display.flip()

page = "menu"
while page != "QUIT":
    if page == "menu":
        page = menu()
    elif page == "PLAY GAME":
        page = game()
    elif page == "HIGH SCORE":
        page = displayHS()
quit()
