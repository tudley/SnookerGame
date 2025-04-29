import game_functions as gf
import restitution_2 as res2
from triangle_collision import find_collision, calc_new_speeds, find_nearest_triangle
import pygame
import sys

# GAME MODULES HOLDS THE MODULES THAT THE MAIN LOOPS THROUGH:
# 1. HANDLE AIMING
# 2. MOVE BALLS
# 3. EVALUATE SHOT
# These 3 modeules are made up from the functions defined within game_functions


def move_balls(balls, cushions, pockets, pocketed_balls, triangles, settings, table):

    """This method moves the balls, once the user has input a power and direction, and clicked shoot
    the balls on the table can collide with eachother, walls, cushion corners, and pockets.
    The balls will slowly decelerate, and be remvoed from the table if potted."""
    
    #check for ball on ball collisions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if gf.check_ball_collision(balls[i], balls[j]):
                    if settings.first_contact == None:
                        settings.first_contact = balls[j].name
                    res2.apply_collission_and_find_new_speeds(balls[i], balls[j], settings)

    #check for horizontal or vertical wall colissions
    for ball in balls:
        gf.check_wall_collission(ball, cushions)

    #check if a ball lands within a pocket
    gf.check_pocket_collision(pockets, balls, pocketed_balls, settings, table)

    #check for 45 degree wall colissions (around pockets)
    for ball in balls:
        nearest_triangle = find_nearest_triangle(ball, triangles)
        if find_collision(nearest_triangle, ball):
            calc_new_speeds(ball, nearest_triangle)

    #slow balls
    gf.apply_friction(balls) 

    #update the balls positions
    gf.update_ball_positions(balls)
    gf.check_for_no_speed(balls, settings)
    #print('the first colour ball that was hit is ', settings.first_contact)


def handle_aiming(settings, balls, white_ball, guideline, ghost_ball, table, screen, cue, pocketed_balls, cue_line):

    """This method is called when they player has to take a shot. This method involved aiming the shot, and assigning the power.
    A guideline and 'ghost ball' will appear and follow the users input, to inform them the of first colissions output trajectories."""
    
    # replace the white ball if it was pocketed
    gf.replace_white(balls, pocketed_balls, white_ball, table, cue_line)

    # set the guidelines startpoint on the cue ball
    guideline.find_startpoint(white_ball)

    # set the attribute 'distance to white ball' for each ball in the balls, this allows the ghostball interact with the first ball it intersects
    balls2 = gf.assign_distances(balls, white_ball)    
    # reorder the balls from furethest to closest to the white ball
    balls2 = gf.order_balls(balls)

    # if player clicks on table, the guideline must be updated
    if settings.aiming == True:

        # find the endpoint of the guidline from the mouse position
        guideline.find_endpoint()

        # update white balls angle attribute to allow for vector velocities to be calculated
        guideline.update_white_balls_angle_attribute(white_ball)

    # draw the guidline
    guideline.draw_full_line(balls2, ghost_ball)

    # if the ghost ball is interacting with another ball, return that ball
    coliding_ball = guideline.draw_ghost_ball(balls2, ghost_ball)

    # if guidline intersects with a ball, draw the ghost ball
    if ghost_ball.active == True:
        ghost_ball.draw()
        gf.draw_colission_paths(white_ball, ghost_ball, coliding_ball, table, settings, screen)

    
    # if the user clicks on the cue, assign power to the shot
    if settings.deciding_power == True:
        mouse_y = pygame.mouse.get_pos()[1]
        gf.assign_power(cue, mouse_y, guideline, white_ball, settings)
    white_ball.convert_velocity_into_x_and_y()


def evaluate_shot(settings, players, balls, choice_button, choice_button2):

    """ This method is called once a the move_balls phase is over, and evaluates the conditions of the next 'aiming' phase.
    Who will take the shot, if they have an advanatge, which colour they are, if they fowled, all of these conditions are evaluated and defined"""

    print('balls pocketed in turn = ')
    for ball in settings.balls_pocketed_in_turn:
        print(ball.name)
    # reset all fouls
    settings.active_player.foul2 = False
    settings.active_player.foul3 = False

    # if player has not been assigned a team
    if settings.active_player.team == None:
        # if player pockets at least one ball
        if len(settings.balls_pocketed_in_turn) > 0:
            #check for fouls
            gf.check_foul1(settings)
            print('foul1 = ', settings.active_player.foul1)
            if settings.active_player.foul1 == False:
                # assign player team to the ball colour
                # if only one ball was pocketed, set the team to that ball colour
                if len(settings.balls_pocketed_in_turn) == 1:
                    print('only one ball potted')
                    settings.active_player.team = settings.balls_pocketed_in_turn[0].name
                    print(f"{settings.active_player.name} has been assigned team {settings.active_player.team}")
                    if settings.balls_pocketed_in_turn[0].name == 'yellow':
                        settings.inactive_player.team = 'red'
                        print(f"{settings.inactive_player.name} has been assigned team {settings.inactive_player.team}")
                        gf.end_evaluation(settings)
                    elif settings.balls_pocketed_in_turn[0].name == 'red':
                        settings.inactive_player.team = 'yellow'
                        print(f"{settings.inactive_player.name} has been assigned team {settings.inactive_player.team}")
                        gf.end_evaluation(settings)
                # if multiple balls were pocketed
                elif len(settings.balls_pocketed_in_turn) > 1:
                    print('multiple balls were pocketed')
                    # evaluate if 2 different colour balls were potted
                    colours = []
                    for ball in settings.balls_pocketed_in_turn:
                        if ball.name not in colours:
                            colours.append(ball.name)
                    if len(colours) == 1:
                        # only one colour ball was potted
                        print(f'only one colour balls was pocketed - {colours[0]}')
                        settings.active_player.team = colours[0]
                        gf.end_evaluation(settings)
                    else:
                        #multiple colours were potted - player can chose which team
                        print('multiple colour balls were pocketed, the player can now select which colour team they would like to play as')
                        settings.player_chose_team = True
                        choice_button2.draw_choice_button() 
                        choice_button.draw_button()    
            else:
                # player has fouled
                print('the player has fouled')
                gf.swap_active_player(players, settings)
                gf.end_evaluation(settings)
        else:
            # player pockets no balls
            #gf.check_foul1(settings)
            if settings.active_player.foul1 == True:
                print('the player has fouled')
                settings.inactive_player.advantage = True
                gf.swap_active_player(players, settings)
                gf.end_evaluation(settings)
            else:
                print('the player has not fouled')
                gf.swap_active_player(players, settings)
                gf.end_evaluation(settings) 


    # if player has been assigned a team
    else:
        gf.check_if_player_has_potted_all_their_balls(settings, balls)
        #gf.check_foul1(settings)
        gf.check_foul2(settings) 
        gf.check_foul3(settings)
        gf.check_for_win(settings)
        if settings.active_player.win == True:
            sys.exit()

        # if player pockets at least one ball
        if len(settings.balls_pocketed_in_turn) > 0:                
            gf.check_gameover(settings)
            print('foul1 = ', settings.active_player.foul1)
            print('foul2 = ', settings.active_player.foul2)
            print('foul3 = ', settings.active_player.foul3)
            print('gameover = ', settings.active_player.gameover)
            if settings.active_player.foul1 == False and settings.active_player.foul2 == False and settings.active_player.foul3 == False:
                # player has not fouled
                print('the player has not fouled')
            else:
                #player has fouled
                print('player has fouled')
                settings.inactive_player.advantage = True
                gf.swap_active_player(players, settings)
            gf.end_evaluation(settings)
        else:
            # player pockets no balls
            if settings.active_player.foul2 == True:
                print('the player has fouled2')
                settings.inactive_player.advantage = True
            gf.swap_active_player(players, settings)
            gf.end_evaluation(settings) 

    # check for win
    gf.check_for_win(settings)
    # check for gameover
    gf.check_gameover(settings)

    settings.foul1 = False  
    settings.inactive_player.advantage = False
    settings.first_contact = None  



