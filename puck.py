import pygame
import random as rand
import math
import constants as const


class Puck:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = const.PUCK_SIZE#퍽의 반경
        self.speed = const.PUCK_SPEED#퍽의 속도
        self.mass = const.PUCK_MASS#퍽의 질량
        self.angle = 0#퍽의 이동각도

    def move(self, time_delta):#퍽의 x축 y축 이동 각도를 정해주고 퍽의 속도를 마찰력과 연결시켜 정해주는 메서드
        self.x += math.sin(self.angle) * self.speed * time_delta
        self.y -= math.cos(self.angle) * self.speed * time_delta
        self.speed *= const.FRICTION

    def check_boundary(self, width, height):#퍽이 경기장 상하좌우에 부딪혔을 때 팅겨져 나오도록 하는 메서드
        # right side
        if self.x + self.radius > width:#width는 경기장 넓이를 말함
            self.x = 2 * (width - self.radius) - self.x#2가아닌 5를하면 마치 가상의 경기장테두리가 있듯이 
            #멀리 가서 안보이다가 팅겨져 나옴
            self.angle = -self.angle

        # left side
        elif self.x - self.radius < 0:
            self.x = 2 * self.radius - self.x
            self.angle = -self.angle

        # bottom
        if self.y + self.radius > height:
            self.y = 2 * (height - self.radius) - self.y
            self.angle = math.pi - self.angle

        # top
        elif self.y - self.radius < 0:
            self.y = 2 * self.radius - self.y
            self.angle = math.pi - self.angle

    def add_vectors(self, angle1, length1, angle2, length2):#게임중 충돌이 일어났을 때 (ex퍽과 패들의 충돌) 그 충돌체들의
        #방향과 속도를 다시 정해 반환해주는 메서드
       
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        
        length = math.hypot(x, y)
        angle = math.pi / 2 - math.atan2(y, x)

        return angle, length

    def collision_paddle(self, paddle):#퍽이 패들과 충돌했을 때 add_vectors메서드를 이용하여
        #퍽의 다음 진행방향과 속도를 정하고 ,충돌후 패들의 이동속도를 정해주고, 또 퍽과 패들이 달라붙지 않게 하는 등
        #퍽과 패들의 충돌 후 상황을 다루는 메서드.
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
        
        # The new vector for puck formed after collision.
        vec_a = (self.angle, self.speed * (self.mass - paddle.mass) / total_mass)
        vec_b = (temp_angle, 2 * paddle.speed * paddle.mass / total_mass)
        
        (self.angle, self.speed) = self.add_vectors(*vec_a, *vec_b)

        # speed should never exceed a certain limit.
        if self.speed > const.MAX_SPEED:
            self.speed = const.MAX_SPEED

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

    def round_reset(self, player):#라운드가 끝났을 때 퍽이 라운드에서 패배한 플레이어 코트쪽에
        #위치하도록 해주는 메서드
        if player == 1:
            self.x = 3*const.WIDTH/4
            
        if player == 2:
            self.x = const.WIDTH/4
        self.y = const.HEIGHT/2
        self.angle = 0
        self.speed = 0

    def reset(self, speed, player):#골을 먹히고 다음 게임이 시작될 때 퍽의 위치가 중앙에서 시작하여 
        #골을 먹힌 플레이어쪽으로 랜덤한 각도를 가지고 이동하도록 해주는 메서드
        if player == 1:
            self.angle = rand.uniform(-math.pi, 0)
        elif player == 2:
            self.angle = rand.uniform(0, math.pi)
        self.speed = speed
        self.x = const.WIDTH / 2
        self.y = const.HEIGHT / 2

    def end_reset(self, speed):#사용자가 설정한 라운드 만큼 게임이 진행 된 후 다시 처음부터 게임을 시작하기 
        #위해 reset을 했을 때의 퍽의 위치가 중앙에서 위아래로 반복운동을 하도록 해주는 메서드
        self.angle = 0
        self.speed = speed
        self.x = const.WIDTH / 2
        self.y = const.HEIGHT / 2

    def draw(self, screen):#화면에 퍽을 나타내주는 메서드
        pygame.draw.circle(screen, const.WHITE, (int(self.x), int(self.y)), self.radius)

    def get_pos(self):#퍽의 x,y좌표를 출력해주는 메서드
        print (self.x, self.y)


