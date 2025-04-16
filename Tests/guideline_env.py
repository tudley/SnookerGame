import pygame
from ball import Ball
from guideline import Guideline
from settings import Settings
import game_functions as gf
import sys
from table import Table

pygame.init()
settings = Settings()
screen = pygame.display.set_mode((800, 500))
table = Table(settings, screen)

balls = []
white_ball = Ball(settings, screen, settings.cue_ball_col)
white_ball.name = 'white'
red_ball = Ball(settings, screen, settings.red_ball_col)
red_ball.name = 'red'
yellow_ball = Ball(settings, screen, settings.yellow_ball_col)
yellow_ball.name = 'yellow'
black_ball = Ball(settings, screen, settings.black_ball_col)
black_ball.name = 'black'
green_ball = Ball(settings, screen, settings.green_ball_col)
green_ball.name = 'green'
balls.append(white_ball)
balls.append(red_ball)
balls.append(yellow_ball)
balls.append(green_ball)
balls.append(black_ball)



white_ball.centerx, white_ball.centery = 250, 200
red_ball.centerx, red_ball.centery = 130, 355
yellow_ball.centerx, yellow_ball.centery = 350, 150
black_ball.centerx, black_ball.centery = 150, 300
green_ball.centerx, green_ball.centery = 110, 400

guideline = Guideline(settings, screen, white_ball, table)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if settings.deciding_shot == True:
                    settings.aiming = True
        elif event.type == pygame.MOUSEBUTTONUP:
            settings.aiming = False

    screen.fill((100, 100, 100))
    table.draw_table()
    for ball in balls:
        ball.draw()
   

    
    ghost_ball = Ball(settings, screen, settings.cue_ball_col, ghost = True)
    #ghost_ball.centerx, ghost_ball.centery = (guideline.endpoint_x, guideline.endpoint_y)
    ghost_ball.centerx, ghost_ball.centery = (0, 0)
    ghost_ball.x_vel, ghost_ball.y_vel = 0, 0
    ghost_ball.name = 'ghost'

    if settings.deciding_shot == True:
        if settings.aiming == True:
            gf.assign_distances(balls, white_ball)
            balls = gf.order_balls(balls)
            guideline.find_endpoint()
            for ball in balls:
                print(ball.name)
            print('end')

            #guideline.draw_guideline()
        guideline.draw_full_line(balls, ghost_ball)

        ghost_ball.draw()

    pygame.display.flip()