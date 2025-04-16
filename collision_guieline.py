import restitution_2 as res2
import pygame

# THIS file governs the white line drawm to screen whilst player is aiming.

def draw_colission_paths(white_ball, ghost_ball, target_ball, table, settings, screen):
    """Draw 2 guidelines showing the path the ghost ball and colliding ball will take once they meet
        NOTE: The target ball is the ball the guideline intersects first"""
    
    # STEP 0: SETUP CONDITIONS

    # ensure the ghosty ball always has a positive speed, so when aiming with 0 power the collision between the ghost ball and the target ball is valid.
    ghost_ball.x_vel = white_ball.x_vel + 0.1
    ghost_ball.y_vel = white_ball.y_vel + 0.1

    #create a copy of the target ball to adjust its velocities to inform the collision path without giving the ball speed
    target_ball_copy = target_ball

    # This use of res2's function of 'simulating the colission' is done with the ghost ball, and the target ball copy, so no 'real' balls attributes are being changed.
    # This function is performed with clone objects to calculate trajectories to show the player the paths the balls will take.
    res2.apply_collission_and_find_new_speeds(ghost_ball, target_ball_copy, settings)



    # STEP 1: CREATE GUIDELINE FROM CUE BALL

    #create the attributes of the guidlines
    try:
        # find the gradient
        ghost_gradient = (ghost_ball.y_vel / ghost_ball.x_vel)
    except:
        # if there is no x velocity, the gradient = infinite
        ghost_gradient = 10**10

    # find the y intercept from equation of a line
    ghost_c = ghost_ball.centery - (ghost_gradient * ghost_ball.centerx)

    # define the startpoint for our guideline
    ghost_startpoint = (ghost_ball.centerx, ghost_ball.centery)

    # find the endpoint of the line
    # if x_vel > 0, ball will travel right so endpoint x will be table right, endpointx can be found from equation of a line
    if ghost_ball.x_vel > 0:
        ghost_endpoint_x = table.rect.right
        ghost_endpoint_y = (ghost_gradient * ghost_endpoint_x) + ghost_c

    # if x_vel < 0, ball will travel left so endpoint x will be table left, endpointx can be found from equation of a line
    elif ghost_ball.x_vel <= 0:
        ghost_endpoint_x = table.rect.left
        ghost_endpoint_y = (ghost_gradient * ghost_endpoint_x) + ghost_c

    # neatly package the endpoint coordinates into one variable
    ghost_endpoint = (ghost_endpoint_x, ghost_endpoint_y)

    # draw the guideline based from our startpoint to our endpoint 
    pygame.draw.line(screen, (255, 255, 255), ghost_startpoint, ghost_endpoint, 3)

    # wipe the velocity components of the ghost ball
    ghost_ball.x_vel = 0
    ghost_ball.y_vel = 0



    # STEP 2: DRAW GUIDELINE FROM TARGET BALL ALONG ITS TRAJECTORY
    
    # find the gradient of the guideline
    try:
        target_gradient = (target_ball.y_vel / target_ball.x_vel)
    except:
        # if target balls x_vel == 0, gradient = infinite
        target_gradient = 10**10

    # find y intercept of guideline from equation of a line
    target_c = target_ball.centery - (target_gradient * target_ball.centerx)

    # define the startpoint of this line
    target_startpoint = (target_ball.centerx, target_ball.centery)

    # if x_vel > 0, ball will travel right so endpoint x will be table right, endpointx can be found from equation of a line
    if target_ball.x_vel > 0:
        target_endpoint_x = table.rect.right
        target_endpoint_y = (target_gradient * target_endpoint_x) + target_c

    # if x_vel < 0, ball will travel left so endpoint x will be table left, endpointx can be found from equation of a line
    elif target_ball.x_vel <= 0:
        target_endpoint_x = table.rect.left
        target_endpoint_y = (target_gradient * target_endpoint_x) + target_c

    # neatly package the endpoint coordinates into one variable
    target_endpoint = (target_endpoint_x, target_endpoint_y)

    # draw guideline for the target ball
    pygame.draw.line(screen, (255, 255, 255), target_startpoint, target_endpoint, 3)

    # reset the target balls velocity components
    target_ball.x_vel = 0
    target_ball.y_vel = 0
