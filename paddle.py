import pygame
import math
import constants as const


class Paddle:#패들의 위치와 이동속도,질량,반경,각도를 초기화 해주는 메서드
    def __init__(self, x, y,s):
        self.x = x
        self.y = y
        self.radius = s#변경 const.PADDLE_SIZE에서 s로 변경
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
       # elif self.x + self.radius > int(width / 2):
            #self.x = int(width / 2) - self.radius #->원래
        elif self.x + self.radius > width:#->추가
            self.x = width - self.radius

    def check_right_boundary(self, width):#플레이어 2 패들의 경계선이 경기장 오른쪽 테두리가 되게끔 설정해주는
        #메서드
        if self.x + self.radius > width:
            self.x = width - self.radius
       # elif self.x - self.radius < int(width / 2):
           # self.x = int(width / 2) + self.radius #->원래
        elif self.x - self.radius <= 0:
            self.x = self.radius

    def move(self, up, down, left, right, time_delta):#패들이 사용자의 키보드 입력에 따라
        #상하좌우와 대각선으로 이동하도록 해주는 메서드
        dx, dy = self.x, self.y
        self.x += (right - left) * self.speed * time_delta
        self.y += (down - up) * self.speed * time_delta

        dx = self.x - dx
        dy = self.y - dy

        self.angle = math.atan2(dy, dx)

    def add_vectors(self, angle1, length1, angle2, length2):
       
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        length = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)

        return angle, length     

    def collision_with_paddle(self, paddle):#퍽이 패들과 충돌했을 때 add_vectors메서드를 이용하여
        #퍽의 다음 진행방향과 속도를 정하고 ,충돌후 패들의 이동속도를 정해주고, 또 퍽과 패들이 달라붙지 않게 하는 등
        #퍽과 패들의 충돌 후 상황을 다루는 메서드. ->새로추가
        """
        Checks collision between circles using the distance formula:
        distance = sqrt(dx**2 + dy**2)
        """
        dx = self.x - paddle.x
        dy = self.y - paddle.y

        # distance between the centers of the circle
        distance = math.hypot(dx, dy)#distance는 퍽과 패들의 거리

        # no collision takes place.
        if distance > self.radius + paddle.radius:
            return False

        # calculates angle of projection.
        tangent = math.atan2(dy, dx)
        temp_angle = math.pi / 2 + tangent
        total_mass = self.mass + paddle.mass
        
        
        # new vector for paddle without changing the speed.
        vec_a = (paddle.angle, paddle.speed * (paddle.mass - self.mass) / total_mass)
        vec_b = (temp_angle + math.pi, 2 * self.speed * self.mass / total_mass)

        temp_speed = paddle.speed
        (paddle.angle, paddle.speed) = self.add_vectors(*vec_a, *vec_b)
        paddle.speed = temp_speed
        #이 구문에 paddle speed를 100을 넣으면 퍽과 패들이 충돌했을떄 패들의 속도가 줄어듬.
        #이구문이없으면 paddle이 퍽과 충돌 후 속도가 변할 수 있음

        
        # To prevent puck and paddle from sticking.
        offset = 0.5 * (self.radius + paddle.radius - distance + 1)
        self.x += math.sin(temp_angle) * offset
        self.y -= math.cos(temp_angle) * offset
        paddle.x -= math.sin(temp_angle) * offset
        paddle.y += math.cos(temp_angle) * offset
        return True     

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
