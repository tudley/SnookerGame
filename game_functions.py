import pygame
import math

    # DRAW_SCREEN FUNCTION - draws all assets

def draw_screen(screen, balls, settings, table, pockets, rails, cushions, pocketed_balls,
                 triangles, lines, button, cue, percentage_button, player_button):
    """Redraw the screen each frame. This is called each loop of the main function"""
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


    # GM.MOVE_BALLS() SUB FUNCTIONS:

def check_pocket_collision(pockets, balls, pocketed_balls, settings, table):
    """Check if the entirety of a ball lies within the area of a pocket, and remove the ball from 'balls' and adds it to 'pocketed balls'.
       This method is called in gm.move_balls()"""
    for ball in balls.copy():
        for pocket in pockets:
            center_to_center_distance = math.sqrt((ball.centerx - pocket.centerx)**2 + (ball.centery - pocket.centery)**2)
            if center_to_center_distance < pocket.radius - ball.radius:
                print(f"{ball.name} has been pocketed into pocket {pocket.position}")
                settings.balls_pocketed_in_turn.append(ball)
                balls.remove(ball)
                pocketed_balls.append(ball)

def check_for_no_speed(balls, settings):
    i = 0
    for ball in balls:
        if ball.x_vel + ball.y_vel == 0:
            i += 1
    if i == len(balls):
        settings.evaluating_shot = True
        settings.moving_balls = False
        settings.turn += 1



# ________GM.EVALUATE_SHOT() SUB FUNCTIONS:___________


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


# UNSURE ABOUT THEIR CLASSIFICATION YET

def check_shoot_button(shoot_button, mouse_x, mouse_y, settings):
    """Check if the mousedown event collides with the shoot button, if so, end gm.handle_aiming() and begin gm.move_balls()"""
    if shoot_button.rect.collidepoint(mouse_x, mouse_y):
        settings.deciding_shot = False
        settings.moving_balls = True


def check_cue_click(cue, mouse_x, mouse_y, settings):
    if cue.border_rect.collidepoint(mouse_x, mouse_y):
        settings.deciding_power = True
        print('deciding power!')


# AIMING SYSTEM FUNCTIONS

def assign_power(cue, mousey,  white_ball, settings):
    # move cue display
    if mousey < cue.border_top:
        cue.cue_top = cue.border_top + 5
    elif cue.border_top + 5 < mousey < cue.border_top + cue.border_height - 5:
        cue.cue_top = mousey
    elif cue.border_top + cue.border_height - 5 < mousey:
        cue.cue_top = cue.border_top + cue.border_height - 5
    cue.update_rects()
    convert_cue_top_to_power_percentage(cue, white_ball, settings)

def convert_cue_top_to_power_percentage(cue, white_ball, settings):
    percentage =  int(100 * ((cue.cue_top - cue.border_top + 5   ) / (cue.border_height - 10   )) - 1.44927536231884)
    print(f"power = {percentage}%")
    cue.percentage = str(percentage)

    white_ball.v_mag = settings.max_speed * percentage/100    










