#!/usr/bin/env python3
# -*- coding utf-8 -*-

import pygame
from pygame.locals import *
from sys import exit
from random import randint

SCREEN_WIDTH=480
SCREEN_HEIGHT=800

pygame.init()
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption('打飞机')

background=pygame.image.load('resources/image/background.png').convert()

# 获取模型图
shootImage=pygame.image.load('resources/image/shoot.png')
#在模型图上截取飞机模型

playerPlaneRect1=pygame.Rect(0,99,102,126)
playerPlaneRect2=pygame.Rect(165,360,102,126)

playerPlaneImage1=shootImage.subsurface(playerPlaneRect1)
playerPlaneImage2=shootImage.subsurface(playerPlaneRect2)

bulletRect=pygame.Rect(1004,987,9,21)
bulletImage=shootImage.subsurface(bulletRect)

enemyRect=pygame.Rect(534,612,57,43)
enemyImage=shootImage.subsurface(enemyRect)

playerPlanePos=[240,680]

class Enemy(pygame.sprite.Sprite):
    '''定义敌人相关信息'''

    def __init__(self,enemy_img,enemy_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=enemy_img
        self.rect=self.image.get_rect()
        self.rect.midbottom=enemy_pos
        self.speed=2

    def update(self):
        if self.rect.top<SCREEN_HEIGHT:
            self.rect.top+=self.speed
        else:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    '''定义子弹相关信息'''

    def __init__(self,bullet_image,bullet_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image=bullet_image
        self.rect=self.image.get_rect()
        self.rect.center=bullet_pos
        self.speed=10

    # 子弹移动
    def update(self):
        if self.rect.bottom>0:
            self.rect.bottom-=self.speed
        else:
            self.kill()

# 定义玩家类 
class PlayerPlane(pygame.sprite.Sprite):
    '''定义玩家类的相关属性'''

    def __init__(self,playerPlane_img,playerPlane_pos):
        '''初始化玩家飞机

        通过加载飞机图片和截取飞机的矩形范围，并通过中心点初始化
        并在图中初始化飞机
        '''
        pygame.sprite.Sprite.__init__(self)

        self.image=playerPlane_img

        self.rect=self.image.get_rect()
        self.rect.center=playerPlane_pos
        self.isHit=False
        self.speed=3
        self.bullets=pygame.sprite.Group()

    # 玩家射击    
    def shoot(self,bullet_img):
        bullet=Bullet(bullet_img,self.rect.midtop)
        self.bullets.add(bullet)

    def move(self):
        '''定义飞机响应键盘按下事件'''
        key_passed=pygame.key.get_pressed()
        if key_passed[pygame.K_w] or key_passed[pygame.K_UP]:
            if self.rect.top<0:
                self.rect.top=0
            else:
                self.rect.top-=self.speed
        if key_passed[pygame.K_s] or key_passed[pygame.K_DOWN]:
            if self.rect.bottom>SCREEN_HEIGHT:
                self.rect.bottom=SCREEN_HEIGHT
            else:
                self.rect.bottom+=self.speed
        if key_passed[pygame.K_a] or key_passed[pygame.K_LEFT]:
            if self.rect.left<0:
                self.rect.left=0
            else:
                self.rect.left-=self.speed
        if key_passed[pygame.K_d] or key_passed[pygame.K_RIGHT]:
            if self.rect.right>SCREEN_WIDTH:
                self.rect.right=SCREEN_WIDTH
            else:
                self.rect.right+=self.speed


playerplane=PlayerPlane(playerPlaneImage1,playerPlanePos)
enemy_group=pygame.sprite.Group()
shoottime=0
clock=pygame.time.Clock()

# 判断敌机和子弹的矩阵碰撞,销毁组
enemy_distory_group=pygame.sprite.Group()

# 判断玩家和敌机的矩阵碰撞，销毁组
player_enemy_distory_group=pygame.sprite.Group()


while True:
    clock.tick(60)
    screen.blit(background,(0,0))
    enemy=Enemy(enemyImage,[randint(int(enemyImage.get_width()/2),SCREEN_WIDTH-
        int(enemyImage.get_width()/2)),0])
    if shoottime %50 ==0:
        enemy_group.add(enemy)
    screen.blit(playerplane.image,playerplane.rect)
    playerplane.move()
    if shoottime %10==0:
        playerplane.shoot(bulletImage)

    enemy_group.update()
    playerplane.bullets.update()
    enemy_group.draw(screen)
    playerplane.bullets.draw(screen)

    #判断子弹和敌机碰撞
    pygame.sprite.groupcollide(enemy_group,playerplane.bullets,True,True)

    #判断玩家和敌机碰撞
    pygame.sprite.spritecollide(playerplane,enemy_group,True)
    pygame.display.update()
    shoottime+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()

while True:
    pass
