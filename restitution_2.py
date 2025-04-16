import math

def apply_collission_and_find_new_speeds(ball_a, ball_b, settings):
    """ This function takes 3 arguments, ball_a, ball_b and the settings object
        The purpose of this function is to be implemented when 2 balls collide
        Then, the speeds and relative positions of eachother are considered, and Newtons restitution equation is used to calculate the speed components
        of both balls post colission. These attributes are then set, and the colission has been simulated.
    """
    # helpful terminal output to ensure correct balls have been recognised as colliding, only occurs when player is not aiming.
    if settings.deciding_shot== False:
        print(f"hit between {ball_a.name} and {ball_b.name}")

    # extract ball attributes for clean code
    ma = ball_a.mass
    mb = ball_b.mass

    #find the contact angle
    delta_x = ball_b.centerx - ball_a.centerx
    delta_y = ball_b.centery - ball_a.centery
    theta = math.atan2(delta_y, delta_x)
    #print('angle of contact = ', math.degrees(theta))
    
    #find the magnitude and angle of the velocities of the balls
    #ball a
    va = math.hypot(ball_a.x_vel, ball_a.y_vel)
    va_theta = math.atan2(ball_a.y_vel, ball_a.x_vel)
    #print('scalar velocity of ball a = ', va)
    #print('velocity angle of ball a = ', math.degrees(va_theta))

    #ball b
    vb = math.hypot(ball_b.x_vel, ball_b.y_vel)
    vb_theta = math.atan2(ball_b.y_vel, ball_b.x_vel)
    #print('scalar velocity of ball b = ', vb)
    #print('velocity angle of ball b = ', math.degrees(vb_theta))

    #find the final x any y velocity components of ball a
    vafx = ((va * (ma - mb) * math.cos(va_theta - theta) + (2 * mb * vb * math.cos(vb_theta - theta))) / (ma + mb)) * math.cos(theta) + (va * math.sin(va_theta - theta) * math.cos(theta + (math.pi / 2)))
    vafy = ((va * (ma - mb) * math.cos(va_theta - theta) + (2 * mb * vb * math.cos(vb_theta - theta))) / (ma + mb)) * math.sin(theta) + (va * math.sin(va_theta - theta) * math.sin(theta + (math.pi / 2)))
   
    #find the final x and y velocity components of ball b
    vbfx = ((vb * (mb - ma) * math.cos(vb_theta - theta) + (2 * ma * va * math.cos(va_theta - theta))) / (ma + mb)) * math.cos(theta) + (vb * math.sin(vb_theta - theta) * math.cos(theta + (math.pi / 2)))
    vbfy = ((vb * (mb - ma) * math.cos(vb_theta - theta) + (2 * ma * va * math.cos(va_theta - theta))) / (ma + mb)) * math.sin(theta) + (vb * math.sin(vb_theta - theta) * math.sin(theta + (math.pi / 2)))

    # convert the magnitude and angle of velocity of ball a and b into their x and y components
    ball_a.x_vel = vafx
    ball_a.y_vel = vafy
    ball_b.x_vel = vbfx
    ball_b.y_vel = vbfy
