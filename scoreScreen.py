import sys

import pygame
import constants
from globals import *
from startScreen import disp_text


def scoreScreen(screen, clock, scr_width, scr_height, music_paused):

    # initialised font
    smallfont = pygame.font.SysFont("comicsans", 35)

    limit = [5,2] #round limit하고 score limit

    if not music_paused:#음악이 정지되어있으면 그대로 정지함.
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#윈도우에 x를 누르면 게임이 꺼진다.
                pygame.quit()
                sys.exit()

        screen.fill((100, 90, 100))#배경 색 RGB로 표현

        # 마우스 데이터 받아오기
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text = smallfont.render("SCORE",True,(28,0,0))
        screen.blit(text,(550,70))#화면에 SCORE라는 글자를 그린다.
        text2 = smallfont.render("ROUND",True,(28,0,0))
        screen.blit(text2,(550,350))#화면에 ROUND라는 글자를 그린다.


        pos_of_polys_right = [[700,130],[700,400]]#화살표위에 투명하게 덧대는 사각형의 위치를 리스트로 저장한다.
        pos_of_polys_left = [[440,130],[440,400]]
        i = 0 #인덱스 변수, 위인지 아래인지 알려고 그냥 선언했다.

        round_num = limit[1]
        score_num = limit[0]
        score_text = smallfont.render(str(score_num),True,(28,0,0))
        round_text = smallfont.render(str(round_num),True,(28,0,0))
        for xy in pos_of_polys_right:
            if(mouse[0]> xy[0]) and (mouse[0] < xy[0]+50) and (mouse[1] > xy[1]) and(mouse[1]<xy[1]+50):
                pygame.draw.polygon(screen,(50,50,50),[[xy[0],xy[1]],[xy[0],xy[1]+50],[xy[0]+50,xy[1]+25]],0)
                if click[0]==1:
                    if i==0:
                        #print("score ++")
                        limit[0] = limit[0] + 1
                    else:
                        #print("round ++")
                        limit[1] = limit[1] + 1
            else:
                pygame.draw.polygon(screen,const.BLACK,[[xy[0],xy[1]],[xy[0],xy[1]+50],[xy[0]+50,xy[1]+25]])#맨 위 오른쪽 삼각형. 색을 배경색과 같이하여 투명하게하였다.
            pygame.draw.rect(screen, const.WHITE,[550,400,90,50])# 그사이의 사각형
            screen.blit(score_text,(585,140))
            screen.blit(round_text,(585,410))
            i = i+1
            

        i = 0
        for xy in pos_of_polys_left:
            if(mouse[0]> xy[0]) and (mouse[0] < xy[0]+50) and (mouse[1] > xy[1]) and(mouse[1]<xy[1]+50):
                pygame.draw.polygon(screen,(50,50,50),[[xy[0]+50,xy[1]],[xy[0]+50,xy[1]+50],[xy[0],xy[1]+25]])
                if click[0]==1:
                    if i==0:
                        #print("score --")
                        if limit[0]==1:
                            continue
                        else:
                            limit[0] = limit[0] - 1
                        
                    else:
                        #print("round --")
                        if limit[1]==1:
                            continue
                        else:
                            limit[1] = limit[1] - 1        
            else:
                pygame.draw.polygon(screen,const.BLACK,[[xy[0]+50,xy[1]],[xy[0]+50,xy[1]+50],[xy[0],xy[1]+25]])#맨 위 왼쪽 삼각형
            pygame.draw.rect(screen, const.WHITE,[550,130,90,50])# 그사이의 사각형
            screen.blit(score_text,(585,140))
            screen.blit(round_text,(585,410))
            i = i+1

        # displaying the selected color
        
        # start
        x, y = width / 2 - 50, 500
        if (mouse[0] > x) and (mouse[0] < x + 90) and (mouse[1] > 500) and (mouse[1] < 530):#start 버튼에 마우스를 갖다댄다면.
            pygame.draw.rect(screen, colors[0][1], (width / 2 - 50, 500, 90, 30), 0) #색이 밝은톤으로 바뀐다.
            if click[0] == 1:
                 return limit
        else:#마우스가 start버튼에 없다면 계속 사각형과 start글자를 그리고있는다.
            pygame.draw.rect(screen, colors[0][0], (width / 2 - 50, 500, 90, 30), 0)
        text_start = smallfont.render("START", True, const.BLACK)
        screen.blit(text_start, [width / 2 - 44, 500])

        #start라고 쓰여진 박스를 그리는 코드
        pygame.display.update()#display 업데이트
        clock.tick(10)# 10fps에서 게임이 돌아감
