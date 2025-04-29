import game_functions as gf

def move_balls(balls, cushions, pockets, pocketed_balls, triangles, settings, table):

    """This method moves the balls, once the user has input a power and direction, and clicked shoot
    the balls on the table can collide with eachother, walls, cushion corners, and pockets.
    The balls will slowly decelerate, and be removed from the table if potted."""
    
    # Ball/Pocket interactions
    gf.check_pocket_collision(pockets, balls, pocketed_balls, settings, table)

    # Ball/Table interactions
    for ball in balls:
        ball.update_ball_position()
        ball.apply_friction()
        ball.check_wall_collission(cushions)
        ball.check_triangle_collission(triangles)

    # Ball/Ball interactions
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball_a = balls[i]
            ball_b = balls[j]
            if ball_a.check_collission_with_ball(ball_b, settings):
                 ball_a.resolve_collission_with(ball_b, settings)

    # Check to end 'move_balls' function once all balls are stationary
    gf.check_for_no_speed(balls, settings)



