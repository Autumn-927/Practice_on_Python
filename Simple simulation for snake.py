# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ref: https://blog.51cto.com/u_15155096/2690582
# 贪食蛇的python简单实现

# 导入部分

import pygame
import sys
import random
import time

## 从pygame中导入键盘控制，事件类型等设置
from pygame.locals import * 

from collections import deque

# 界面的基础数值设置

## 单位方格大小
unit_size = 20    

screen_height, screen_width = 480, 600
line_width = 1  

## 坐标取值范围
x_range = (0,screen_width//unit_size - 1)
y_range = (2,screen_height//unit_size - 1)

## 部分自定义颜色设置
red_color = (200,30,30)
black_color = (0,0,0)
light_color = (100,100,100)
dark_color = (200,200,200)
background_color = (40,40,60)

## 设置统一的文本输出格式

def print_txt(screen,font,x,y,txt,fcolor = (255,255,255)):
    output = font.render(txt,True,fcolor)
    screen.blit(output,(x,y))

# 食物的基础设置

## 食物种类: 决定分值和颜色
food_type_list = [(10,(255,100,100)),\
    (20,(100,255,100)),(50,(100,100,255))]

## 随机出现位置: 注意排除食物出现在蛇身的情况
def create_food_position(snake):
    x = random.randint(x_range[0],x_range[1])
    y = random.randint(y_range[0],y_range[1])
    while (x,y) in snake:
        x = random.randint(x_range[0],x_range[1])
        y = random.randint(y_range[0],y_range[1])
    return x,y

## 随机出现种类
def create_food_type():
    return food_type_list[random.randint(0,2)]

# 蛇的基础设置

## 初始状态
def init_snake():
    snake = deque()
    snake.append((2,y_range[0]))
    snake.append((1,y_range[0]))
    snake.append((0,y_range[0]))
    return snake

# 进入游戏时的具体设置
def main():
    ## 初始化一个准备显示的窗口
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))

    ## 设置标题
    pygame.display.set_caption('贪食蛇')

    ## 设置基本字体
    font1 = pygame.font.SysFont('SimHei',24)
    font2 = pygame.font.SysFont('SimHei',72)

    ## 创建防止摁键过快产生的bug
    turnbug = True

    ## 创造初始状态的蛇和食物
    snake = init_snake()
    food_position = create_food_position(snake)
    food_type = create_food_type()

    ##创建初始方向
    direction = (1,0)

    ## 启动游戏的变量初始化
    game_over = True
    game_start = False
    pause = False
    score = 0
    init_speed = 0.1
    speed = init_speed
    last_move_time = None

    ## 开始游戏

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
                
            ### 键盘输入
            elif event.type == KEYDOWN:

                if event.key == K_RETURN:

                    if game_over:   # 省略if game_over == True
                        game_start = True
                        game_over = False
                        turnbug = True

                        snake = init_snake()
                        food_position = create_food_position(snake)
                        food_type = create_food_type()
                        direction = (1,0)

                        score = 0
                        last_move_time = time.time()

                elif event.key == K_SPACE:

                    if not game_over:
                        pause = not pause

                elif event.key in (K_UP,K_w):
                    if turnbug and not direction[1]:
                        direction = (0,-1)
                        turnbug = False
                elif event.key in (K_DOWN,K_s):
                    if turnbug and not direction[1]:
                        direction = (0,1)
                        turnbug = False
                elif event.key in (K_LEFT,K_a):
                    if turnbug and not direction[0]:
                        direction = (-1,0)
                        turnbug = False
                elif event.key in (K_RIGHT,K_d):
                    if turnbug and not direction[0]:
                        direction = (1,0)
                        turnbug = False
            
        ## 填充背景色
        screen.fill(background_color)

        ## 画网格线
        for x in range(unit_size,screen_width,unit_size):
            pygame.draw.line(screen,black_color,(x,y_range[0] * unit_size),(x,screen_height),line_width)
        for y in range(y_range[0] * unit_size,screen_height,unit_size):
            pygame.draw.line(screen,black_color,(0,y),(screen_width,y),line_width)

        ## 蛇的运动过程
        if not game_over:
            current_time = time.time()
            if current_time - last_move_time > speed:
                if not pause:
                    turnbug = True
                    last_move_time = current_time
                    next_step = (snake[0][0] + direction[0],\
                        snake[0][1] + direction[1])

                    ### 如果吃到食物
                    if next_step == food_position:
                        snake.appendleft(next_step)
                        score += food_type[0]
                        speed = init_speed + 0.01 * (score//100)
                        food_position = create_food_position(snake)
                        food_type = create_food_type()
                        
                    else:
                        if x_range[0] <= next_step[0] <= x_range[1] and\
                            y_range[0] <= next_step[1] <= y_range[1] and\
                                next_step not in snake:
                                snake.appendleft(next_step)
                                snake.pop()
                        else:
                            game_over = True
            
        ## 画出蛇和食物
        if not game_over:
            pygame.draw.rect(screen,food_type[1],\
                (food_position[0] * unit_size,food_position[1] * unit_size,\
                    unit_size,unit_size),0)
        for s in snake:
            pygame.draw.rect(screen,dark_color,\
                (s[0] * unit_size + line_width,s[1] * unit_size + line_width,\
                    unit_size - line_width * 2,unit_size - line_width * 2),0)
        print_txt(screen,font1,30,7,f'速度: {speed}')
        print_txt(screen,font1,450,7,f'分数: {score}')
            
        ## 游戏结束
        if game_over:
            if game_start:
                print_txt(screen,font2,screen_width//4,\
                    screen_height//4,\
                        '游戏结束',red_color)
            
        pygame.display.update()

if __name__ == '__main__':
    main()

            



    


    










