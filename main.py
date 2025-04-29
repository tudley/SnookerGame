import pygame
import pygame.font
from settings import Settings
from ball import Ball
import sys
import game_functions as gf
import game_modules as gm
from table import Table
from pocket import Pocket
from game_objects import Rail
from game_objects import Cushion
from game_objects import Triangle
from game_objects import Line
from button import Button, Choice_button
from guideline import Guideline
from cue import Cue
from player import Player
from aiming_system import AimingSystem

import shot_decision as sd

pygame.init()

# create all the objects for the game
clock = pygame.time.Clock()
settings = Settings()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
table = Table(settings, screen)

# create the individual pockets and add them to a list of pockets 
pockets = []
mid_right_pocket = Pocket(settings, screen, table, 'midright')
mid_left_pocket = Pocket(settings, screen, table, 'midleft')
top_right_pocket = Pocket(settings, screen, table, 'topright')
top_left_pocket = Pocket(settings, screen, table, 'topleft')
bottom_right_pocket = Pocket(settings, screen, table, 'botright')
bottom_left_pocket = Pocket(settings, screen, table, 'botleft')
pockets.append(mid_right_pocket)
pockets.append(mid_left_pocket)
pockets.append(top_right_pocket)
pockets.append(top_left_pocket)
pockets.append(bottom_right_pocket)
pockets.append(bottom_left_pocket)

# this is the background around the table
rails = Rail(settings, screen, table, mid_right_pocket)

# create the balls
white_ball = Ball(settings, screen, settings.cue_ball_col)
yellow_ball = Ball(settings, screen, settings.yellow_ball_col)
red_ball = Ball(settings, screen, settings.red_ball_col)
yellow_ball2 = Ball(settings, screen, settings.yellow_ball_col)
red_ball2 = Ball(settings, screen, settings.red_ball_col)
black_ball = Ball(settings, screen, settings.black_ball_col)

ghost_ball = Ball(settings, screen, settings.cue_ball_col, ghost = True)
ghost_ball.centerx, ghost_ball.centery = (0, 0)
ghost_ball.name = 'ghost'

balls = []
balls.append(white_ball)
balls.append(yellow_ball)
balls.append(red_ball)
balls.append(yellow_ball2)
balls.append(red_ball2)
balls.append(black_ball)

# create an empty list to add the pocketed balls to
pocketed_balls = []

# create guide lines
lines = []
cue_line = Line('cue line', settings, screen, table)
black_spot = Line('black spot', settings, screen, table)
lines.append(cue_line)
lines.append(black_spot)

# create the 'triangles' which make up the edges of the cushions
triangles = []
triangle_tl_t = Triangle('topleft top', table, top_left_pocket, settings, screen)
triangle_t_l = Triangle('top left', table, top_left_pocket, settings, screen)
triangle_t_r = Triangle('top right', table, top_right_pocket, settings, screen)
triangle_tr_t = Triangle('topright top', table, top_right_pocket, settings,screen)
triangle_tl_b = Triangle('topleft bot', table, mid_left_pocket, settings, screen)
triangle_tr_b = Triangle('topright bot', table, mid_right_pocket, settings, screen)
triangle_bl_t = Triangle('botleft top', table, mid_left_pocket, settings, screen)
triangle_br_t = Triangle('botright top', table, mid_right_pocket, settings, screen)
triangle_bl_b = Triangle('botleft bot', table, bottom_left_pocket, settings, screen)
triangle_br_b = Triangle('botright bot', table, bottom_right_pocket, settings, screen)
triangle_b_l = Triangle('bot left', table, bottom_left_pocket, settings, screen)
triangle_b_r = Triangle('bot right', table, bottom_right_pocket, settings, screen)
triangles.append(triangle_tl_t)
triangles.append(triangle_t_l)
triangles.append(triangle_t_r)
triangles.append(triangle_tr_t)
triangles.append(triangle_tl_b)
triangles.append(triangle_tr_b)
triangles.append(triangle_bl_t)
triangles.append(triangle_br_t)
triangles.append(triangle_bl_b)
triangles.append(triangle_br_b)
triangles.append(triangle_b_l)
triangles.append(triangle_b_r)

# create the walls for the ball to bounce off
cushions = []

top_cushion = Cushion(settings, screen, table, top_left_pocket, 'top', 'top', top_right_pocket)
top_left_cushion = Cushion(settings, screen, table, top_left_pocket, 'left', 'topleft', mid_left_pocket)
top_right_cushion = Cushion(settings, screen, table, top_right_pocket, 'right', 'topright', mid_right_pocket)
bot_left_cushion = Cushion(settings, screen, table, mid_left_pocket, 'left', 'botleft', bottom_left_pocket)
bot_right_cushion = Cushion(settings, screen, table, mid_right_pocket, 'right', 'botright', bottom_right_pocket)
bot_cushion = Cushion(settings, screen, table, bottom_left_pocket, 'bot', 'bot', bottom_right_pocket)
cushions.append(top_cushion)
cushions.append(top_left_cushion)
cushions.append(top_right_cushion)
cushions.append(bot_left_cushion)
cushions.append(bot_right_cushion)
cushions.append(bot_cushion)


# place the balls on the screen
white_ball.centerx, white_ball.centery = (table.rect.centerx - 100, table.rect.centery - 200)
yellow_ball.centerx, yellow_ball.centery = (table.rect.centerx, table.rect.centery)
yellow_ball.x_vel = 10
red_ball.centerx, red_ball.centery = (table.rect.centerx - red_ball.radius - 30, table.rect.centery - 25)
yellow_ball2.centerx, yellow_ball2.centery = (table.rect.centerx - 120, table.rect.centery + 100)
red_ball2.centerx, red_ball2.centery = (table.rect.centerx + red_ball.radius + 30, table.rect.centery + 200)
black_ball.centerx, black_ball.centery = (table.rect.centerx + red_ball.radius + 5, table.rect.centery - 45)


# create the cue visual
cue = Cue(settings, screen)

# create the 2 players
player1 = Player('player 1')
player2 = Player('player 2')
players = [player1, player2]
settings.active_player = players[0]
settings.inactive_player = players[1]

# create the buttons
shoot_button = Button(settings, screen, 'shoot', settings.shoot_rect)
guideline = Guideline(settings, screen, white_ball, table)
percentage_button = Button(settings, screen, cue.percentage, settings.percentage_rect)
choice_button = Button(settings, screen, 'Please chose the colour', settings.choice1_rect)
choice_button2 = Choice_button(settings, screen, 'you wish to play as:', settings.choice2_rect)
player_button = Button(settings, screen, (settings.active_player.name + 'team: ' +  str(settings.active_player.team) + '. advantage: ' +  str(settings.active_player.advantage)), settings.player_rect)
player_button.font = pygame.font.SysFont(None, 28)

# Here I create the AimingSystem object, to handle the aiming phase of the game
aiming_system = AimingSystem(settings, table, screen, guideline, cue, pocketed_balls, balls, white_ball, cue_line, ghost_ball)

def rungame():
    
    while True:

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    gf.check_shoot_button(shoot_button, mouse_x, mouse_y, settings)
                    gf.check_cue_click(cue, mouse_x, mouse_y, settings)
                    if settings.player_chose_team == True:
                        gf.check_choice_button(mouse_x, mouse_y, choice_button, settings)
                    if settings.deciding_shot == True:
                        if table.rect.left < mouse_x < table.rect.right and table.rect.top < mouse_y < table.rect.bottom:
                            settings.aiming = True
                elif event.button == 3:
                    white_ball.centerx, white_ball.centery = mouse_x, mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                settings.aiming = False 
                settings.deciding_power = False


        #draw the screen
        gf.draw_screen(screen, balls, settings, table, pockets, rails, cushions, pocketed_balls, triangles, lines, shoot_button, cue, percentage_button, player_button)
   
        #handle the 'deciding shot' phase
        if settings.deciding_shot == True:  
            aiming_system.aim()

        # handle the 'balls moving' phase    
        if settings.moving_balls == True:
            gm.move_balls(balls, cushions, pockets, pocketed_balls, triangles, settings, table)

        # handle evaluating balls phase
        if settings.evaluating_shot == True:
            sd.evaluate_shot(settings, players, balls, choice_button, choice_button2)
            
        pygame.display.flip()
        clock.tick(60)
  
rungame()

