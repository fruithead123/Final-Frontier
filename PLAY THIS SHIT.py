from pygame import *
from math import *
from random import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from ex5 import *





#--------Stat-up screen



#-----Google Api------------
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Game").sheet1
list_of_values = sheet.get_all_values()

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
        self.IFrames = 200

        self.trail = []


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
        self.trail.append([self.x, self.y])
        if len(self.trail) > 100:
            self.trail = self.trail[1:]

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

        if self.velocity < 0.025 and self.velocity > 0:
            self.velocity = 0
        if self.velocity > -0.025 and self.velocity < 0:
            self.velocity = 0

        if self.aVelocity < 0.025 and self.aVelocity > 0:
            self.aVelocity = 0
        if self.aVelocity > -0.025 and self.aVelocity < 0:
            self.aVelocity = 0

    def rota(self, angle):
        self.aVelocity += angle
        if self.aVelocity > 2:
            self.aVelocity = 2
        if self.aVelocity < -2:
            self.aVelocity = -2

    def rotate(self, ang = 0):
        newP = []
        for i in self.points:
            oX = i[0] - self.x
            oY = i[1] - self.y
            a = radians(self.aVelocity)
            newP.append([(oX * cos(a + ang) + oY * sin(a+ ang)) + self.x, (-oX * sin(a+ ang) + oY * cos(a+ ang)) + self.y])
        self.dir += self.aVelocity
        self.points = newP

        if self.aVelocity > 0:
            self.aVelocity -= 0.1
        if self.aVelocity < 0:
            self.aVelocity += 0.1

    def draw(self, s):
        '''
        bSurface = Surface((88, 88))
        bSurface.set_alpha(100)
        draw.circle(bSurface, (255,255,255), (44, 44), 30, 0)
        screen.blit(bSurface, (self.x-44, self.y-44))
        '''
        vert = [[ int(i[0]), int(i[1]) ] for i in self.points]
        draw.polygon(s, (255,255,255), vert, 3)

        b =Surface((1080,720),SRCALPHA)

        for i in range(1,len(self.trail), 20):
            l = self.trail[i]
            draw.circle(b, (255,255,255, 2*i), (int(l[0]), int(l[1])), 5)

        screen.blit(b, (0,0))

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
    def __init__(self, x, y, ang, time, type):
        self.x = x
        self.y = y
        self.dir = float(ang)
        self.time = time
        self.type = type


    def move(self):
        dx = self.time*cos(radians(self.dir+90))
        dy = self.time*sin(radians(self.dir+90))
        self.x -= dx
        self.y += dy
        self.time = max(2, self.time - 0.05)

    def draw(self, s):
        #[int(self.x-(i*2)), int(self.y-(i*2))]
        dx = cos(radians(self.dir+90))
        dy = sin(radians(self.dir+90))
        bul = Surface((22,22))
        transform.rotate(bul, self.dir)
        bul.fill((0,0,0))
        if self.type == 0:
            for i in range(5):
                draw.circle(bul, (255,255-(i*51),0), (6+(i*3),16-(i*3)), 6-i)
                a = transform.rotate(bul, self.dir + 50)
                screen.blit(a, (self.x-11, self.y-11))
        else:
            for i in range(5):
                draw.circle(bul, (255-(i*51),255,0), (6+(i*3),16-(i*3)), 6-i)
                a = transform.rotate(bul, self.dir + 50)
                screen.blit(a, (self.x-11, self.y-11))


class Square:           # A type of enemy
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hp = 10
        self.RhombusPoints = [[x,y-25],[x+25,y+25],[x,y+25],[x-25,y]]
        self.RectPoints = [[x-25,y-25],[x+25,y-25],[x+25,y+25],[x-25,y+25]]
        self.dir = randint(0,360)
        self.ang = 0
        self.shotCooldown = randint(25,100)

    def draw(self, s):
        #draw.rect(screen,(124,252,0),Rect(self.x,self.y,50,50),1)
        #pt1,pt2,pt3,pt4 = [self.x+25,self.y],[self.x+50,self.y+25],[self.x+25,self.y+50],[self.x,self.y+25]
        #draw.polygon(screen,(125,252,0),[pt1,pt2,pt3,pt4],1)
        draw.polygon(s,(125,252,0),self.RectPoints,1)
        draw.polygon(s,(125,252,0),self.RhombusPoints,1)

    def checkHit(self, bulletx, bullety):
        return Rect(self.x-25,self.y-25,50,50).collidepoint(bulletx, bullety)

    def rotate(self, angle = 0):
        newP = []
        self.ang += 5
        t = self.ang
        newP.append([self.x+25*sqrt(2)*cos(radians(45+t)),self.y+25*sqrt(2)*sin(radians(45+t))])
        newP.append([self.x+25*sqrt(2)*cos(radians(135+t)),self.y+25*sqrt(2)*sin(radians(135+t))])
        newP.append([self.x+25*sqrt(2)*cos(radians(225+t)),self.y+25*sqrt(2)*sin(radians(225+t))])
        newP.append([self.x+25*sqrt(2)*cos(radians(315+t)),self.y+25*sqrt(2)*sin(radians(315+t))])
        self.RectPoints = newP
        newP=[]
        newP.append([self.x+25*cos(radians(t)),self.y+25*sin(radians(t))])
        newP.append([self.x+25*cos(radians(90+t)),self.y+25*sin(radians(90+t))])
        newP.append([self.x+25*cos(radians(180+t)),self.y+25*sin(radians(180+t))])
        newP.append([self.x+25*cos(radians(270+t)),self.y+25*sin(radians(270+t))])
        self.RhombusPoints = newP


    def trans(self):
        if self.x > 1080:
            #self.setPos(0, self.y)
            self.x = self.x-1080
            for i in self.RectPoints:
                i[0] = i[0]-1080
            for i in self.RhombusPoints:
                i[0] = i[0]-1080
        if self.x < 0:
            #self.setPos(1080, self.y)
            self.x = 1080+self.x
            for i in self.RectPoints:
                i[0] = i[0]+1080
            for i in self.RhombusPoints:
                i[0] = i[0]+1080
        if self.y > 720:
            #self.setPos(self.x, 0)
            self.y = self.y-720
            for i in self.RectPoints:
                i[1] = i[1]-720
            for i in self.RhombusPoints:
                i[1] = i[0]-720
        if self.y < 0:
            #self.setPos(self.x, 720)
            self.y = 720 +self.y
            for i in self.RectPoints:
                i[1] = i[1]+720
            for i in self.RhombusPoints:
                i[1] = i[1]+720
    def move (self):
        #no one will read this but kevin is big dummy
        dy = randint(1,10)/10*cos(radians(self.dir))
        dx = randint(1,10)/10*sin(radians(self.dir))
        newP=[]
        for i in self.RhombusPoints:
            newP.append([dx+i[0],dy+i[1]])

        self.RhombusPoints = newP
        newP=[]

        for i in self.RectPoints:
            newP.append([dx+i[0],dy+i[1]])

        self.RectPoints = newP


        self.x += dx
        self.y += dy

class Triangle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.points = [(x + 15,y-15), (x-15,y-15), (x,y+21)]
        self.dir = randint(0,360)
        self.shotCooldown = randint(20,50)

    def move(self):
        dy = 2*cos(radians(self.dir))
        dx = 2*sin(radians(self.dir))
        self.x += dx
        self.y += dy
        newP = []
        for i in self.points:
            newP.append([i[0] + dx, i[1] + dy])
        self.points = newP

    def rotate(self, ang):
        newP = []
        for i in self.points:
            oX = i[0] - self.x  #Shift to the origin
            oY = i[1] - self.y
            a = radians(ang)    #Rotation angle
            newP.append([(oX * cos(a) + oY * sin(a)) + self.x, (-oX * sin(a) + oY * cos(a)) + self.y])
            #The signs in front of the sins are flipped to account for pygame axis
        self.dir += ang
        self.points = newP

    def draw(self, s):
        vert = [[ int(i[0]), int(i[1]) ] for i in self.points]
        draw.polygon(s, (0,255,0), vert, 3)
    def trans(self):
        pass
    def checkHit(self, bulletx, bullety):
        return Rect(self.x-15,self.y-21,30,45).collidepoint(bulletx, bullety)




class Explosion:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.dir = randint(0,360)
        self.velocity = randint(4,5)
        self.col = col


    def move(self):
        dx = self.velocity*cos(radians(self.dir))
        dy = self.velocity*sin(radians(self.dir))
        self.x += dx
        self.y += dy
        self.velocity = max(1, self.velocity - 0.2)

    def draw(self, s):
        draw.line(s, self.col, (self.x, self.y), (self.x + 15*cos(radians(self.dir)), self.y + 15*sin(radians(self.dir))), 3)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~ Game ~~~~~~~~~~~~~~~~~~~~~~~~
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
init()
mixer.init()
mixer.set_num_channels(32)
size=(1080, 720)
screen=display.set_mode(size)
display.set_caption("Bad Game 2: Final Frontier")
scoreFont = font.SysFont("Ailerons", 35)
labelFont = font.SysFont("Ailerons", 50)
hsFont = font.SysFont("Ailerons", 70)
titleFont = font.SysFont("Ailerons", 40)
titleFont2 = font.SysFont("Ailerons", 70)
score = 0
pewpew = mixer.Sound("snd\laser3.ogg")
mixer.music.load("snd\menu.ogg")

def createScrollStars(maxStars,surface):
    'Creates the initial starfield in levels (2D)'
    stars=[]
    for i in range(maxStars):
        star=[randint(0,1080),randint(0,720),randint(1,100)] #[x,y,speed]
        if star[2]<60: #60% chance to move 1 unit per frame
            star[2]=1
        elif star[2]<95: #35% chance to move 1.5 units per frame
            star[2]=1.5
        else:           #5% chance to move 2 units per frame
            star[2]=2
        stars.append(star)
    return stars

def moveDrawStars(stars,surface, dx = 0,dy = 0):
    'Updates the starfield in levels'
    for star in stars:
        star[1] += (star[2] - 0.005*dy) #Add star speed to y coord (Only move downwards)
        star[0] -= 0.005*dx

        #Reset stars if offscreen
        if star[1]>=720: #If the star goes offscreen, generate another one
            star[1]=0
            star[0]=randint(0,1080-1)
            star[2]=choice([1,1.5,2])
        if star[1] < 0:
            star[1] = 720
        if star[0] > 1080:
            star[0] = 0
        if star[0] < 0:
            star[0] = 1080

        #Set color depending on speed
        if star[2]==1:
          color=(100,100,100) #Stars moving slower are less visible
        elif star[2]==1.5:
          color=(150,150,150)
        elif star[2]==2:
          color=(200,200,200)

        draw.circle(surface,color,[int(star[0]),int(star[1])],int(star[2]))

scrollStarList=createScrollStars(500,screen)

def menu():
    mixer.music.fadeout(1000)
    mixer.music.load("snd\menu.ogg")
    mixer.music.set_volume(1)
    mixer.music.play(-1)
    running = True
    fps = time.Clock()
    titleCap = titleFont.render("BAD GAME 2", 1, (255,255,255))
    titleCap2 = titleFont2.render("FINAL FRONTIER", 1, (255, 255, 255))
    beginCap = labelFont.render("Start Game", 1, (0,0,0))
    highCap = labelFont.render("High Scores", 1, (0,0,0))
    quitCap = labelFont.render("Quit", 1, (0,0,0))
    buttons = [Rect(290, y * 80 + 360, 500, 65) for y in range(3)]
    text = ["PLAY GAME", "HIGH SCORE", "QUIT"]

    plr = Player()
    #plr.rotate(180)
    plr.setPos(540,300)
    maxSize = 200
    while running:
        fps.tick    
        for evnt in event.get():
            if evnt.type == QUIT:
                return "QUIT"
        mpos = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.fill((0,0,0))
        moveDrawStars(scrollStarList, screen)
        for r, v in zip(buttons, text):
            draw.rect(screen, (255, 255, 255), r)
            screen.blit(titleCap, (290, 100))
            screen.blit(titleCap2, (260, 130))
            screen.blit(beginCap, (390, 360))
            screen.blit(highCap, (370, 440))
            screen.blit(quitCap, (485, 520))
            if (r.collidepoint(mpos)):
                draw.rect(screen, (5, 100, 255), r, 3)
                if (mb[0] == 1):
                    screen.fill((0,0,0))
                    return v
        plr.draw(screen)
        display.flip()

def game():
    global score
    mixer.music.fadeout(1000)
    mixer.music.set_volume(0.5)
    mixer.music.load("snd\moonlord.mp3")
    mixer.music.play(-1)
    running = True
    fps = time.Clock()
    plr = Player()
    plr.setPos(540, 360)
    plrBullets = []
    enemyBullets = []
    squareEnemy = []
    explosions = []
    multiplier = 1
    score = 0


    for i in range(randint(4,8)):
        squareEnemy.append(Square(randint(0,1080),randint(0,720)))
        squareEnemy.append(Triangle(randint(0,1080),randint(0,720)))

    while running:
        fps.tick(80)
        for evt in event.get():
            if evt.type == QUIT:
                return 'QUIT'
        score += 0.01
        scoreCap = scoreFont.render("SCORE: " + str(int(score)), 1, (255, 255, 255))
        healthCap = scoreFont.render("HEALTH: " + str(plr.hp), 1, (255, 255, 255))
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        keys = key.get_pressed()
        if plr.IFrames > 0:
            plr.IFrames -= 1
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
            plrBullets.append(Bullet(plr.x, plr.y, plr.dir-3, 8, 0))
            plrBullets.append(Bullet(plr.x, plr.y, plr.dir, 8, 0))
            plrBullets.append(Bullet(plr.x, plr.y, plr.dir+3, 8, 0))
            plr.shotCooldown = 25
            mixer.Sound.play(pewpew)
        if keys[K_ESCAPE]:
            return 'menu'

        screen.fill((0,0,0))
        moveDrawStars(scrollStarList, screen, plr.x - 540, plr.y - 360)

        for b in plrBullets:
            if b.x > 1100 or b.x < -20 or b.y > 740 or b.y < -20:
                plrBullets.remove(b)
            else:
                b.move()
                b.draw(screen)

        for b in enemyBullets:
            if b.x > 1100 or b.x < -20 or b.y > 740 or b.y < -20:
                enemyBullets.remove(b)
            else:
                b.move()
                b.draw(screen)

        if len(squareEnemy) < 5:
            if randint(0,1) == 1:
                squareEnemy.append(Square(randint(0,1080), randint(0,720)))
            else:
                squareEnemy.append(Triangle(randint(0,1080), randint(0,720)))
        for e in squareEnemy:
            e.draw(screen)
            e.rotate(2)
            e.move()
            e.trans()
            for b in plrBullets:
                if e.checkHit(b.x, b.y):
                    col = choice([(255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0)])
                    for i in range(100):
                        explosions.append(Explosion(e.x, e.y, col))
                    if e in squareEnemy:
                        squareEnemy.remove(e)
                    plrBullets.remove(b)
                    multiplier += 0.01
                    score += int(100*multiplier)
            for b in enemyBullets:
                if plr.x - 5< b.x <plr.x + 5 and plr.y < b.y < plr.y + 5 and plr.IFrames == 0:
                    col = choice([(255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0)])
                    for i in range(100):
                        explosions.append(Explosion(e.x, e.y, col))
                    plr.hp -= 1
                    plr.IFrames = 200

            if e.checkHit(plr.x, plr.y) and plr.IFrames == 0:
                col = choice([(255,255,255), (255,0,0), (0,0,255), (0,255,0), (255,255,0)])
                for i in range(100):
                    explosions.append(Explosion(e.x, e.y, col))
                plr.hp -= 1
                plr.IFrames = 100

            if e.shotCooldown > 0:
                e.shotCooldown -= 1
                if e.shotCooldown == 0:
                    enemyBullets.append(Bullet(e.x,  e.y, randint(0,360), 15, 1))
                    e.shotCooldown = randint(10,50) #i like shirts and free underwear. - david zucc"erberg"ini jin(ny boy)

        if plr.hp == 0:
            saveScore()
            endGame(score)

        plr.move()
        plr.trans()
        plr.rotate()
        plr.draw(screen)

        if plr.shotCooldown > 0:
            plr.shotCooldown -= 1

        for e in explosions:
            e.move()
            if e.velocity < randint(2,3):
                explosions.remove(e)
            else:
                e.draw(screen)

        screen.blit(scoreCap, (0,0))
        screen.blit(healthCap, (890, 0))
        display.flip()

def readScore():
    file = open("score.txt")
    score = file.readlines()
    for i in range (3):
        score[i] = score[i].strip("\n")
    file.close()
    return score

def saveScore():
    global score,list_of_values
    score = int(score)
    n = len(list_of_values)
    sheet.update_cell(n+1,1,str(name.get()))
    sheet.update_cell(n+1,2,score)

    list_of_values = sheet.get_all_values()



def endGame(endScore):
    screen.fill((0,0,0))
    endFont = font.SysFont("Ailerons", 80)
    endCap = endFont.render("YOU DIED!", 1, (255, 255, 255))
    endCap2 = endFont.render("YOUR SCORE: " + str(endScore), 1, (255, 255, 255))
    endCap3 = endFont.render("PRESS ESC TO RESTART", 1, (255, 255, 255))

    running = True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                return "QUIT"
        screen.blit(endCap, (350, 130))
        screen.blit(endCap2, (170, 280))
        screen.blit(endCap3, (80, 500))
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            return "menu"
        display.flip()




def displayHS():
    
    dic = [[k,int(v)] for (k,v) in list_of_values]
    dic.sort(key = lambda x: x[1],reverse = True)
    fps = time.Clock()
    scores = readScore()
    running = True
    counter = 0
    while running:
        fps.tick(80)
        for evt in event.get():
            if evt.type == QUIT:
                return "QUIT"
        screen.fill((0,0,0))
        moveDrawStars(scrollStarList, screen)
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            return "menu"

        for i in range(5):

            screen.blit(hsFont.render(dic[i][0] + ". " + str(dic[i][1]),1,(255,255,255)), (250, 180 + 80 * i))
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
