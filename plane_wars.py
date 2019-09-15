import pygame
import sys
import random
import time

#!!!!必须在游戏窗口的主题中写上监听事件的循环，否则游戏窗口会不响应

"""初始化"""
pygame.init()
pygame.display.init()
pygame.mixer.init()
pygame.font.init()
#print(pygame.font.get_default_font())

"""设置"""
pygame.display.set_caption("飞机大战")
s_width = 600
s_hight = 800
p_speed = 10
#飞机初始位置
p_x = 400
p_y = 600-95
#子弹的设置
b_speed = 0.5
x, y = (p_x+34), p_y-20
grade = 0

movel = False
mover = False
active = False
game_over = False
start = True

#示例化一个装敌机的容器和一个装子弹的容器
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#3个继承自精灵的类
class Plane(pygame.sprite.Sprite):
    def __init__(self,plane,screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = plane
        self.rect = self.image.get_rect()

        #绘制的初始位置
        self.x = 400
        self.y = 600-95

        self.screen = screen

    def move(self, movel, mover):
        if movel and self.x >= 0:
            self.x -= p_speed
        if self.x <= 720 and mover:
            self.x += p_speed

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        #绘制
        self.screen.blit(self.image, (self.x, self.y))

class Eplane(pygame.sprite.Sprite):
    def __init__(self,e_plane,screen):
        pygame.sprite.Sprite.__init__(self)
        #print(type(self.rect))
        #print("敌机的rect属性",self.rect)

        #初始绘制位置
        self.x = random.randint(0,600)
        self.y = 0

        #self.rect = (300,0)
        self.screen = screen

        #精灵对象要求的基本属性
        self.image = e_plane
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        #敌机下落速度
        self.speed = 2

    def update(self):
        if self.y <= 600:
            self.y = self.y + self.speed
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            self.screen.blit(self.image,(self.x,self.y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,bullet, screen, x):
        pygame.sprite.Sprite.__init__(self)
        #self.r_plane = r_plane
        self.screen = screen

        #初始绘制位置
        self.x = x+34
        self.y = p_y-10

        #本精灵对象的基本属性
        self.image = bullet
        #self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        #print("子弹的rect属性",self.rect)

        #子弹的初始速度
        self.speed = 2

    def update(self, *args):
        if self.y>= 0:
            self.y = self.y-self.speed
            self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
            self.screen.blit(self.image, (self.x, self.y))
"""
#定义碰撞检测函数
def collide(value1, value2):
    if value1.x == value2.x and value1.y == value2.y:
        return True
    else:
        return False
"""

#创建必要的surface对象
screen = pygame.display.set_mode((s_hight,s_width))
ground = pygame.image.load("1.jpg")
plane = pygame.image.load("3.jpg")
enemy_plane = pygame.image.load("4.jpg")
bullet = pygame.Surface([4,10])

#自定义的一个事件
GEN = pygame.USEREVENT+1
# 设置要在程序中捕捉的事件
pygame.time.set_timer(GEN, 4000)

#示例化一个敌机精灵并添加到队列中的函数
def add_enemy():
    enemy_sprite = Eplane(enemy_plane,screen)
    enemy_group.add(enemy_sprite)

#enemy_sprite = Eplane(enemy_plane,screen)
#enemy_group.add(enemy_sprite)

#游戏时钟对象
clock = pygame.time.Clock()

#获得飞机的矩形对象
#r_plane = plane.get_rect()
#print(r_plane)
# 实例化一个子弹的矩形对象
#bullet = pygame.Rect((x, y), (6, 15))
#获得敌机的矩形对象
#r_enemy = enemy_plane.get_rect()

#测试变量
rank = 1

# 实例化一个飞机精灵对象
s_plane = Plane(plane, screen)

#实例化一个字体对象
font_1 = pygame.font.Font("freesansbold.ttf", 80)
font_2 = pygame.font.Font("freesansbold.ttf", 20)
#需要用到的字体对象
s_font = font_1.render("play", True, (100, 100, 100), (0, 0, 0))
e_font = font_1.render("restart", True, (100, 100, 100), (0, 0, 0))

# 刷新帧率设置
clock.tick(60)

while True:
    screen.blit(ground, (0, 0))

    if game_over:
        screen.blit(e_font, (300, 200))

        #清除上一把的数据
        enemy_group.empty()
        bullet_group.empty()
        grade = 0

        active = False

        #事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    e_x, e_y = event.pos
                    #print(e_x,e_y, type(e_x))
                    if 300<=int(e_x)<=550 and 200<=int(e_y)<=280:
                        active = True
                        game_over = False
                        #print(type(event.pos), event.button)
        #显示页面
        pygame.display.flip()

    #s_plane.update()
    #screen.blit(plane, (p_x, p_y))
    #screen.blit(enemy_plane,(300,0))

    #绘制敌机
    #enemy_group.update()
    #enemy_group.draw(screen)

    #pygame.draw.rect(screen, (0, 0, 0), bullet)

    #碰撞和出界检测
    elif active:
        #绘制计分牌
        g_font = font_2.render("grade:{}".format(grade), True, (100, 100, 100), (0, 0, 0))
        screen.blit(g_font,(10,10))

        if pygame.sprite.groupcollide(bullet_group, enemy_group, True, True):
            grade += 1
        if pygame.sprite.spritecollide(s_plane, enemy_group, True):
            pygame.mixer.music.load("8.mp3")
            pygame.mixer.music.play(1,0.0)

            game_over = True

        #print(len(enemy_group.sprites()))
        for enemy in enemy_group.sprites():
            #print("敌机",enemy.x, enemy.y)
            #print(enemy.y)
            if enemy.y >= 600:
                enemy_group.remove(enemy)
                #print("干的漂亮，敌机%d坠毁了"%rank)
                #print(len(enemy_group.sprites()))
                rank = rank+1
        for b in bullet_group.sprites():
            #print("子弹", b.x, b.y)
            if b.y <= 0:
                bullet_group.remove(b)

        if pygame.mixer.music.get_busy() == False:
            #加载音乐
            pygame.mixer.music.load("5.mp3")
            pygame.mixer.music.play(1,0.0)


        #检测事件
        for event in pygame.event.get():
            num = 1
            if event.type == GEN and num == 1:
                add_enemy()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movel = True

                if event.key == pygame.K_RIGHT:
                    mover = True

                if event.key == pygame.K_SPACE:
                    bullet_sprite = Bullet(bullet, screen, s_plane.x)
                    bullet_group.add(bullet_sprite)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    movel = False
                if event.key == pygame.K_RIGHT:
                    mover = False

        #绘制飞机
        s_plane.move(movel, mover)

        #绘制敌机
        enemy_group.update()

        #绘制子弹
        bullet_group.update()

        """
        #移动
        if movel and p_x >= 0:
            p_x -= p_speed

        if p_x <= 720 and mover:
            p_x += p_speed
        """

        #刷新屏幕显示
        pygame.display.flip()

    elif start:
        screen.blit(s_font, (300, 200))

        active = False

        # 事件监听
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    e_x, e_y = event.pos
                    # print(e_x,e_y, type(e_x))
                    if 300 <= int(e_x) <= 550 and 200 <= int(e_y) <= 280:
                        active = True
                        start = False
                        # print(type(event.pos), event.button)
        # 显示页面
        pygame.display.flip()
