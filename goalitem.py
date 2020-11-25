import constants as const
import pygame
import math
import os
from globals import *

class Goalitem():

    def __init__(self,x,y):
        #super(Goalitem,self).__init__()
        self.image=pygame.image.load(os.path.join(auxDirectory, 'warp.png'))
        self.x=x
        self.y=y
        self.radius=self.image.get_rect()
   
        
    #def draw(self, screen):#화면에 아이템을 나타내주는 메서드 
        #pygame.draw.circle(screen, const.PURPLE, (int(self.x), int(self.y)), self.radius)
        
    #def delete(self):
        #pygame.sprite.Group.empty(self)
        #pygame.draw.visible(False)
        

    def check_vertical_bounds(self, height):#경기장 위아래 경계를 지정하여 아이템이 그 경계를 못 넘어가도록
        #해주는 메서드
        # top radius를 잠깐 radius.height로 바꾸겠음
        if self.y - self.radius.height <= 0:
            self.y = self.radius.height
        # bottom
        elif self.y + self.radius.height > height:
            self.y = height - self.radius.height

    def check_boundary(self, width):#아이템의 경계선이 경기장이 되게끔 설정해주는
        #메서드
        if self.x - self.radius.width <= 0:
            self.x = self.radius.width
       # elif self.x + self.radius > int(width / 2):
            #self.x = int(width / 2) - self.radius #->원래
        elif self.x + self.radius.width > width:#->추가
            self.x = width - self.radius.width

    def reset(self, start_x, start_y):#라운드가 끝나거나 게임이 리셋될 때 아이템의 위치를 처음 초기화 시킨 좌표에
        #위치시켜주는 메서드
        self.x = start_x
        self.y = start_y


    def effect_A(self,paddle):

        #self.radius를 self.radius.width로 바꿔봄 한번
        dx = self.x - paddle.x
        dy = self.y - paddle.y
        distance = math.hypot(dx, dy)
        if distance > self.radius.width + paddle.radius:
            return False

        elif distance < 3*(self.radius.width + paddle.radius)/4:
            #const.PADDLE_SIZE=60
            const.PADDLE_SIZEA+=5
            return True

    def effect_B(self,paddle):

        
        dx = self.x - paddle.x
        dy = self.y - paddle.y
        distance = math.hypot(dx, dy)
        if distance > self.radius.width + paddle.radius:
            return False

        elif distance < 3*(self.radius.width + paddle.radius)/4:
            #const.PADDLE_SIZE=60 ->원래꺼
            const.PADDLE_SIZEB+=5 #실험용 ->성공
            
            return True
        

            


