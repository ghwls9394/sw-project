import pygame
import math
import constants as const


class Paddle:#패들의 위치와 이동속도,질량,반경,각도를 초기화 해주는 메서드
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = const.PADDLE_SIZE
        self.speed = const.PADDLE_SPEED
        self.mass = const.PADDLE_MASS
        self.angle = 0

    def check_vertical_bounds(self, height):#경기장 위아래 경계를 지정하여 패들이 그 경계를 못 넘어가도록
        #해주는 메서드
        # top
        if self.y - self.radius <= 0:
            self.y = self.radius
        # bottom
        elif self.y + self.radius > height:
            self.y = height - self.radius

    def check_left_boundary(self, width):#플레이어 1 패들의 경계선이 경기장 왼쪽 테두리가 되게끔 설정해주는
        #메서드
        if self.x - self.radius <= 0:
            self.x = self.radius
        elif self.x + self.radius > int(width / 2):
            self.x = int(width / 2) - self.radius

    def check_right_boundary(self, width):#플레이어 2 패들의 경계선이 경기장 오른쪽 테두리가 되게끔 설정해주는
        #메서드
        if self.x + self.radius > width:
            self.x = width - self.radius
        elif self.x - self.radius < int(width / 2):
            self.x = int(width / 2) + self.radius

    def move(self, up, down, left, right, time_delta):#패들이 사용자의 키보드 입력에 따라
        #상하좌우와 대각선으로 이동하도록 해주는 메서드
        dx, dy = self.x, self.y
        self.x += (right - left) * self.speed * time_delta
        self.y += (down - up) * self.speed * time_delta

        dx = self.x - dx
        dy = self.y - dy

        self.angle = math.atan2(dy, dx)

    def draw(self, screen, color):#화면에 패들을 초기화 시킨 위치와 반경 ,색상 값을 가지고 위치시킨다.
        position = (int(self.x), int(self.y))

        pygame.draw.circle(screen, color, position, self.radius, 0)
        pygame.draw.circle(screen, (0, 0, 0), position, self.radius, 2)
        pygame.draw.circle(screen, (0, 0, 0), position, self.radius - 5, 2)
        pygame.draw.circle(screen, (0, 0, 0), position, self.radius - 10, 2)
        

    def get_pos(self):#패들의 x,y좌표를 반환해주는 메서드
        return self.x, self.y

    def reset(self, start_x, start_y):#라운드가 끝나거나 게임이 리셋될 때 패들의 위치를 처음 초기화 시킨 좌표에
        #위치시켜주는 메서드
        self.x = start_x
        self.y = start_y
