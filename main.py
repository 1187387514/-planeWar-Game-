import pygame,sys
from pygame.locals import *
import random
import pygame.freetype

pygame.init()
width = 400
height = 600
#这里设置可拉伸屏幕，下面事件里需要想要的处理
screen = pygame.display.set_mode((width,height),pygame.RESIZABLE)
pygame.display.set_caption("宇宙飞机大战")
icon = pygame.image.load("data/life.png")
pygame.display.set_icon(icon)
fclock = pygame.time.Clock()
backgroud = pygame.image.load('data/background.png')
over = pygame.image.load('data/gameover.png')
#导入背景音乐并播放
pygame.mixer.music.load("backmusic.ogg")
pygame.mixer.music.play()
#增加音乐播放完的事件
OVER = USEREVENT
pygame.mixer.music.set_endevent(OVER)
#子弹图片
bullet_img1 = pygame.image.load('data/bullet1.png')
bullet_img2 = pygame.image.load('data/bullet2.png')
#玩家飞机图片
player_imgs=[]
for i in range(1,3):
    player_imgs.append(pygame.image.load(f'data/me{i}.png'))
#玩家飞机被击毁图片
player_down_imgs = []
for i in range(1,5):
    player_down_imgs.append(pygame.image.load(f'data/me_destroy_{i}.png'))
    print(player_down_imgs)
#敌机1图片
enemy1_imgs = pygame.image.load('data/enemy1.png')
#敌机1被击毁图片
enemy1_down_imgs = []
for i in range(1,5):
    enemy1_down_imgs.append(pygame.image.load(f'data/enemy1_down{i}.png'))
#敌机2图片
enemy2_imgs = pygame.image.load('data/enemy2.png')
#敌机2发射图片
enemy2_hit_imgs = pygame.image.load('data/enemy2_hit.png')
#敌机2被击毁图片
enemy2_down_imgs = []
for i in range(1,5):
    enemy2_down_imgs.append(pygame.image.load(f'data/enemy2_down{i}.png'))
#敌机3图片
enemy3_imgs = []
for i in range(1,3):
    enemy3_imgs.append(f'data/enemy3_n{i}.png')
#敌机3发射图片
enemy3_hit_imgs = pygame.image.load('data/enemy3_hit.png')
#敌机2被击毁图片
enemy3_down_imgs = []
for i in range(1,7):
    enemy3_down_imgs.append(pygame.image.load(f'data/enemy3_down{i}.png'))
#读取文件
def readfile(path):
    with open(path,"r") as f:
        row = f.readline()
        res = row.split(":")
        return res
#写入文件
def writefile(content,way,path):
    with open(path,way) as f:
        f.write(content)
#子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self,img,init_pos):
        pygame.sprite.Sprite.__init__(self)
        # 传进来图片参数已经load过，这里直接引用就可以
        self.image = img.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed
#玩家飞机类
class Player(pygame.sprite.Sprite):
    def __init__(self,imgs,down_imgs,init_pos):
        pygame.sprite.Sprite.__init__(self)
        # 图片用列表是因为它不是一张图而是一个动画
        self.images = []
        for i in imgs:
            # 可以设置可透明
            self.images.append(i.convert_alpha())
        self.down_images = []
        for i in down_imgs:
            # 可以设置可透明
            self.down_images.append(i.convert_alpha())
        self.rect = self.images[0].get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
        self.bullets = pygame.sprite.Group()
        self.is_hit = False
        self.img_index = 0

    def shoot(self,bullet_img):
        bullet = Bullet(bullet_img,self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top == 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom >= height:
            self.rect.bottom == height
        else:
            self.rect.bottom += self.speed

    def moveLeft(self):
        if self.rect.left+self.rect.width/2 <= 0:
            self.rect.left = -self.rect.width/2
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right-self.rect.width/2 >= width:
            self.rect.right = width+self.rect.width/2
        else:
            self.rect.right += self.speed
#敌机1类
class Enemy1(pygame.sprite.Sprite):
    def __init__(self,img,down_imgs,init_pos,max_speed=2):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha()
        self.down_imgs = []
        for i in down_imgs:
            self.down_imgs.append(i.convert_alpha())
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = random.randint(1,max_speed)
        self.down_index = 0

    def move(self):
        self.rect.bottom += self.speed

def startGame():
    player_init_pos = [200,600]
    player = Player(player_imgs,player_down_imgs,player_init_pos)
    bullet_frequence = 0
    enemy1_frequence = 0
    player_down_frequence = 0
    enemy1_group = pygame.sprite.Group()
    enemy1_down_group = pygame.sprite.Group()
    score = 0


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == OVER:
                pygame.mixer.music.play()
            #如果希望只能按一下才能移动一步的话采用下面注释的写法
            # if event.type == pygame.KEYDOWN:
            #     if event.key == K_w or event.key == K_UP:
            #         player.moveUp()
            #     elif event.key == K_s or event.key == K_DOWN:
            #         player.moveDown()
            #     elif event.key == K_a or event.key == K_LEFT:
            #         player.moveLeft()
            #     elif event.key == K_d or event.key == K_RIGHT:
            #         player.moveRight()
        #希望长按键盘能移动就用下面的写法
        keypress = pygame.key.get_pressed()
        if keypress[K_w] or keypress[K_UP]:
            player.moveUp()
        elif keypress[K_s] or keypress[K_DOWN]:
            player.moveDown()
        elif keypress[K_a] or keypress[K_LEFT]:
            player.moveLeft()
        elif keypress[K_d] or keypress[K_RIGHT]:
            player.moveRight()
        screen.fill((0,0,0))
        screen.blit(backgroud,(0,0))
        #一定频率生成敌机并移动
        score_rank = score // 1000
        if enemy1_frequence % max((50-score_rank*10),1) == 0:
            enemy1_init_pos = [random.randint(0,width-enemy1_imgs.get_size()[0]),0]
            enemy1 = Enemy1(enemy1_imgs,enemy1_down_imgs,enemy1_init_pos,score_rank+2)
            enemy1_group.add(enemy1)
        enemy1_frequence+=1
        if enemy1_frequence == 50:
            enemy1_frequence = 0

        #移动敌机并判断是否碰撞
        for enemy1 in enemy1_group:
            enemy1.move()
            if enemy1.rect.top > height:
                enemy1_group.remove(enemy1)
            if pygame.sprite.collide_circle(player,enemy1):
                enemy1_group.remove(enemy1)
                enemy1_down_group.add(enemy1)
                player.is_hit = True
        enemys1_down = pygame.sprite.groupcollide(enemy1_group,player.bullets,True,True)
        for enemy_down in enemys1_down:
            #如果不在敌机列表里删除会有什么变化
            # enemy1_group.remove(enemy_down)
            enemy1_down_group.add(enemy_down)
        #迭代销毁数组，显示1号敌机爆炸动画
        for enemy_down in enemy1_down_group:
            if enemy_down.down_index > 7:
                enemy1_down_group.remove((enemy_down))
                score+=100
                continue
            screen.blit(enemy_down.down_imgs[enemy_down.down_index//2],enemy_down.rect)
            enemy_down.down_index+=1
        enemy1_group.draw(screen)
        #游戏得分
        f1 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc",36)
        f1.render_to(screen,[0,0],str(score),fgcolor=(255,251,0),size=25)
        #游戏难度等级
        f2 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc",36)
        f2.render_to(screen, [screen.get_rect().right-80, screen.get_rect().bottom-36], "难度:"+str(score_rank+1), fgcolor=(255, 251, 0), size=25)
        #判断玩家是否被击中，没有则发射子弹和显示
        if not player.is_hit:
            if bullet_frequence%15 == 0:
                player.shoot(bullet_img1)
            bullet_frequence+=1
            if bullet_frequence == 15:
                bullet_frequence = 0
            player.img_index = bullet_frequence//8
            screen.blit(player.images[player.img_index],player.rect)
        else:
            if player_down_frequence <32:
                screen.blit(player.down_images[player_down_frequence//8],player.rect)
                player_down_frequence+=1
            else:
                running = False
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom <= 0 :
                player.bullets.remove(bullet)
        player.bullets.draw(screen)
        fclock.tick(60)
        pygame.display.update()
    #显示结束画面
    # screen.blit(over,[width/2-150,height/2-150])
    f1 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    f1.render_to(screen, (screen.get_rect().centerx - 180, screen.get_rect().centery - 100), "GAME OVER",
                 fgcolor=(255, 0, 125), size=60)
    f2 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    f2.render_to(screen, (screen.get_rect().centerx - 100, screen.get_rect().centery), "得分：" + str(score) + "分",
                 fgcolor=[0, 0, 0], size=36)
    f3 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    f3.render_to(screen, (screen.get_rect().centerx - 80, screen.get_rect().centery + 130), "重新开始",
                 fgcolor=(255, 125, 125), size=36)
    f4 = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    f4.render_to(screen, (screen.get_rect().centerx - 65, screen.get_rect().centery + 190), "排行榜",
                 fgcolor=(88, 20, 125), size=36)
    print(f4.get_rect("排行榜").left, f4.get_rect("排行榜").right, f4.get_rect("排行榜").height)

    #获取排行榜信息并更新排行版
    rank = readfile("score.txt")
    temp = 0
    for i in range(len(rank)):
        if int(rank[i])<score:
            print(int(rank[i]),score)
            temp = rank[i]
            rank[i] = str(score)
            score = 0
        if int(rank[i]) < int(temp):
            rank[i],temp = temp,rank[i]
    writefile(":".join(rank),"w","score.txt")

def rankdisplay():
    screen2 = pygame.display.set_mode((width,height),pygame.RESIZABLE)
    screen2.fill((0, 0, 0))
    screen2.blit(backgroud, (0, 0))
    #重新开始
    fa = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    fa.render_to(screen2, (screen2.get_rect().centerx - 80, screen2.get_rect().centery + 130), "重新开始",
                 fgcolor=(255, 125, 125), size=36)
    #排行榜
    fb = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
    fb.render_to(screen2, (screen2.get_rect().centerx - 65, 10), "排行榜",
                 fgcolor=(255, 75, 125), size=36)
    rank = readfile("score.txt")
    ranklist = [str(i) for i in range(1,11)]
    for i in range(len(rank)):
        f = pygame.freetype.Font("C:\Windows\Fonts\msyh.ttc", 36)
        f.render_to(screen2,(screen2.get_rect().centerx - 100, 25+35*(i+1)),f"第{ranklist[i]}名:"+rank[i],fgcolor=(150, 0, 125), size=36)

startGame()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #判断鼠标点击位置来进行重新开始游戏
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if screen.get_rect().centerx +70 > event.pos[0] > screen.get_rect().centerx - 80 \
                        and screen.get_rect().centery + 130 < event.pos[1] <screen.get_rect().centery + 166:
                    startGame()
                elif screen.get_rect().centerx +45 > event.pos[0] > screen.get_rect().centerx - 65 \
                        and screen.get_rect().centery + 190 < event.pos[1] <screen.get_rect().centery + 225:
                    rankdisplay()
        elif event.type == OVER:
            pygame.mixer.music.play()

    pygame.display.update()
