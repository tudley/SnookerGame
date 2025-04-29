import pygame
import math
from triangle_collision import find_collision, calc_new_speeds, find_nearest_triangle
import restitution_2 as res2
from collision_guieline import draw_colission_paths
import sys

def draw_screen(screen, balls, settings, table, pockets, rails, cushions, pocketed_balls, pocket_hitbox,
                 triangles, lines, button, ghost_ball, cue, percentage_button, player_button):
    """Redraw the screen each frame"""

    # fill background
    screen.fill(settings.bg_colour)

    # draw rails
    rails.draw_rail()

    # draw table
    table.draw_table()

    # draw table marking lines
    for line in lines:
        line.draw_line()

    # draw_cushions
    for cushion in cushions:
        cushion.draw_cushion()

    # draw cushion corners
    for triangle in triangles:
        triangle.draw_triangle()

    # draw pockets
    for pocket in pockets:
        pocket.draw_pocket() 

    # draw pocketed balls
    i = 0
    for ball in pocketed_balls:
        i += 1
        pygame.draw.circle(screen, ball.colour, (settings.screen_width - (settings.screen_width - table.width)/4, 2 * i * ball.radius), ball.radius)

    # draw active balls
    for ball in balls:
        ball.draw()

    # draw the cue
    cue.draw_border()
    cue.draw_cue()

    # draw the shoot button
    button.draw_button()

    # update the percentage button text, and draw the button
    percentage_button.prep_msg(cue.percentage)
    percentage_button.draw_button()

    # update the player button and draw it
    player_button.prep_msg(settings.active_player.name + 'team: ' +  str(settings.active_player.team) + '. advantage: ' +  str(settings.active_player.advantage))
    player_button.draw_button()


def update_ball_positions(balls):
    "move all the balls"
    for ball in balls:

        # update the centers
        ball.centerx += ball.x_vel
        ball.centery += ball.y_vel
        ball.centerx = float(ball.centerx)
        ball.centery = float(ball.centery)

        # update the corners
        for phi in range(-16, 16, 1):
            num = phi/16
            phi *= math.pi / 32
            corner = (ball.centerx + ball.radius * math.cos(phi), ball.centery + ball.radius * math.sin(phi))
            ball.corners[num] = (corner)

        # OUTDATED method of using 4 manually set corners
        """
        ball.tl = (ball.centerx - ball.radius * math.sin(ball.phi), ball.centery - ball.radius * math.sin(ball.phi))
        ball.tr = (ball.centerx + ball.radius * math.sin(ball.phi), ball.centery - ball.radius * math.sin(ball.phi))
        ball.bl = (ball.centerx - ball.radius * math.sin(ball.phi), ball.centery + ball.radius * math.sin(ball.phi))
        ball.br = (ball.centerx + ball.radius * math.sin(ball.phi), ball.centery + ball.radius * math.sin(ball.phi))
        #update the corner dictionary
        ball.corners['tl'] = ball.tl
        ball.corners['tr'] = ball.tr
        ball.corners['bl'] = ball.bl
        ball.corners['br'] = ball.br
        """


def apply_friction(balls):
    """reduce the speed of the balls to model friction"""

    for ball in balls:
        if abs(ball.x_vel) > 0.1:
            ball.x_vel *= 0.994
        else:
            ball.x_vel = 0
        
        if abs(ball.y_vel) > 0.1:
            ball.y_vel *= 0.994
        else:
            ball.y_vel = 0


def check_wall_collission(ball, cushions):
    """check if a ball hits the edge of the table, and adjust the balls velocity appropriately"""
    ball_r_edge = ball.centerx + ball.radius
    ball_l_edge = ball.centerx - ball.radius
    ball_t_edge = ball.centery - ball.radius
    ball_b_edge = ball.centery + ball.radius

    for cushion in cushions:
        if cushion.side == 'left':
            if ball.centery < cushion.rect.bottom and ball.centery > cushion.rect.top:
                if ball_l_edge <= cushion.rect.right:
                    ball.x_vel *= -1
        
        if cushion.side == 'right':
            if ball.centery < cushion.rect.bottom and ball.centery > cushion.rect.top:
                if ball_r_edge >= cushion.rect.left:
                    ball.x_vel *= -1
        
        if cushion.side == 'top':
            if ball.centerx < cushion.rect.right and ball.centerx > cushion.rect.left:
                if ball_t_edge <= cushion.rect.bottom:
                    ball.y_vel *= -1
        
        if cushion.side == 'bot':
            if ball.centerx < cushion.rect.right and ball.centerx > cushion.rect.left:
                if ball_b_edge >= cushion.rect.top:
                    ball.y_vel *= -1


def check_ball_collision(ball1, ball2):
    """Check if 2 balls have touched"""
    dist_between_centers = math.sqrt((ball1.centerx - ball2.centerx)**2 + (ball1.centery - ball2.centery)**2)
    if dist_between_centers <= ball2.radius + ball1.radius:
        return True


def check_pocket_collision(pockets, balls, pocketed_balls, settings, table):
    """Check if the entirety of a ball lies within the area of a pocket, and remove the ball"""
    for ball in balls.copy():
        for pocket in pockets:
            center_to_center_distance = math.sqrt((ball.centerx - pocket.centerx)**2 + (ball.centery - pocket.centery)**2)
            if center_to_center_distance < pocket.radius - ball.radius:
                print(f"{ball.name} has been pocketed into pocket {pocket.position}")
                settings.balls_pocketed_in_turn.append(ball)
                balls.remove(ball)
                pocketed_balls.append(ball)


def check_shoot_button(shoot_button, mouse_x, mouse_y, settings):
    """check if the mousedown event collides with the shoot button"""
    if shoot_button.rect.collidepoint(mouse_x, mouse_y):
        settings.deciding_shot = False
        settings.moving_balls = True


def assign_distances(balls, white_ball):
    """assign an attribute for each ball containing the distance between the centers of the ball and the cue ball"""
    for ball in balls:
        if ball.name != 'white':
            distance_to_white = math.sqrt((ball.centerx - white_ball.centerx)**2 + (ball.centery - white_ball.centery)**2)
            ball.distance_to_white = distance_to_white
            

def order_balls(balls):
    """reorder the list of balls from closest to furthest from the white ball"""
    new_list = sorted(balls, key = lambda x : x.distance_to_white, reverse = False)
    return new_list


def check_for_no_speed(balls, settings):
    i = 0
    for ball in balls:
        if ball.x_vel + ball.y_vel == 0:
            i += 1
    if i == len(balls):
        settings.evaluating_shot = True
        settings.moving_balls = False
        settings.turn += 1

def cal_shot_angle(mouse_x, mouse_y, startpoint_y, startpoint_x):
    theta = math.atan2((mouse_y - startpoint_y) / (mouse_x - startpoint_x))
    return theta

def check_cue_click(cue, mouse_x, mouse_y, settings):
    if cue.border_rect.collidepoint(mouse_x, mouse_y):
        settings.deciding_power = True
        print('deciding power!')

def convert_cue_top_to_power_percentage(cue, white_ball):

    percentage =  int(100 * ((cue.cue_top - cue.border_top + 5   ) / (cue.border_height - 10   )) - 1.44927536231884)
    print(f"power = {percentage}%")
    cue.percentage = str(percentage)

    white_ball.v_mag = 10 * percentage/100
    

def assign_power(cue, mousey, guideline,  white_ball, settings):
    
    # move cue display
    if mousey < cue.border_top:
        cue.cue_top = cue.border_top + 5
    elif cue.border_top + 5 < mousey < cue.border_top + cue.border_height - 5:
        cue.cue_top = mousey
    elif cue.border_top + cue.border_height - 5 < mousey:
        cue.cue_top = cue.border_top + cue.border_height - 5
    cue.update_rects()
    convert_cue_top_to_power_percentage(cue, white_ball)


def reset_shot_stats(settings):
    settings.first_contact = None

def check_foul1(settings):
    """check if player pots the white ball"""
    for ball in settings.balls_pocketed_in_turn:
        #print(ball.name)
        if ball.name == "white":
            settings.active_player.foul1 = True
            print(settings.active_player.name, ' has potted the white')


def check_foul2(settings):
    """check if the player hits the opponents ball first"""
    if settings.first_contact == settings.inactive_player.team:
        settings.active_player.foul2 = True
        print(settings.active_player.name, ' has hit the opponents ball first')
        return True
    else:
        return False

def check_foul3(settings):
    """check if the player pockets an opponents ball"""
    for ball in settings.balls_pocketed_in_turn:
        if ball.name == settings.inactive_player.team:
            settings.active_player.foul3 = True
            print(settings.active_player.name, 'has pocketed their opponents ball')

def check_foul4(settings):
    if settings.first_contact == None:
        settings.active_player.foul4 = True
        print(settings.active_player.name, ' did not make contact with any balls')
        return True
    else:
        return False

def check_gameover(settings):
    # method 1: player is not yet supposed to pot the black yet does
    if settings.active_player.team != 'black':
        for ball in settings.balls_pocketed_in_turn:
            if ball.name == 'black':
                settings.active_player.gameover = True
                print(f"{settings.active_player.name} has potted the black before they should - gameover!")

    # method 1: player is on the black yet pockets another ball along with it
    if settings.active_player.team == 'black':
        if len(settings.balls_pocketed_in_turn) > 1:
            for ball in settings.balls_pocketed_in_turn:
                if ball.name != 'black':
                    settings.active_player.gameover = True
                    print(f"{settings.active_player.name} potted the bacl with another ball and loses.")



def check_if_player_has_potted_all_their_balls(settings, balls):
    """assigns a player to team 'black' if the pot all their colour balls"""
    remaining_team_balls = 0
    for ball in balls:
        #print(ball.name)
        if ball.name == settings.active_player.team:
            remaining_team_balls += 1
    if remaining_team_balls == 0:
        print('player has potted all their balls and now needs to pot the black')
        settings.active_player.team = 'black'

def give_advantage(settings):
    settings.inactive_player.advantage = True


def swap_active_player(players, settings):
    if settings.active_player == players[0]:
        settings.active_player = players[1]
        settings.inactive_player = players[0]
    elif settings.active_player == players[1]:
        settings.active_player = players[0]
        settings.inactive_player = players[1]


def end_evaluation(settings):
    settings.evaluating_shot = False
    settings.deciding_shot = True
    for ball in settings.balls_pocketed_in_turn.copy():
        settings.balls_pocketed_in_turn.remove(ball)


def check_choice_button(mousex, mousey, choice_button, settings):
    distance_from_mouse_to_red_ball = math.sqrt((mousex - settings.red_ball_center[0])**2 + (mousey - settings.red_ball_center[1])**2)
    distance_from_mouse_to_yellow_ball = math.sqrt((mousex - settings.yellow_ball_center[0])**2 + (mousey - settings.yellow_ball_center[1])**2)

    if distance_from_mouse_to_red_ball < settings.ball_radius * 2:
        settings.active_player.team = 'red'
        settings.inactive_player.team = 'yellow'
        end_evaluation(settings)
    elif distance_from_mouse_to_yellow_ball < settings.ball_radius * 2:
        settings.active_player.team = 'yellow'
        settings.inactive_player.team = 'red'
        end_evaluation(settings)

def check_for_win(settings):
    if settings.active_player.team == 'black':
        if settings.active_player.foul1 == False and settings.active_player.foul2 == False and settings.active_player.foul3 == False:
            if len(settings.balls_pocketed_in_turn) == 1:
                if settings.balls_pocketed_in_turn[0].name == 'black':
                    settings.active_player.win = True
                    print(f"{settings.active_player.name} has won the game")

# HANDLE AIMING FUNCTIONS:

def replace_white(balls, pocketed_balls, white_ball, table, cue_line):
    replace_white = False
    for ball in pocketed_balls.copy():
        if ball.name == 'white':
            pocketed_balls.remove(ball)
            replace_white = True
    if replace_white == True:
        white_ball.centerx, white_ball.centery = table.rect.centerx, cue_line.start_point[1]
        balls.append(white_ball)







