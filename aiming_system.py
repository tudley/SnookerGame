from collision_guieline import draw_colission_paths
import pygame
import game_functions as gf

class AimingSystem:
    """Handles the aiming phase of the game, including cue ball placement, aiming, and power assignment."""
    
    def __init__(self, settings, table, screen, guideline, cue, pocketed_balls, balls, white_ball, cue_line, ghost_ball):
        self.settings = settings
        self.table = table
        self.screen = screen
        self.guideline = guideline
        self.cue = cue
        self.balls = balls
        self.pocketed_balls = pocketed_balls
        self.white_ball = white_ball
        self.cue_line = cue_line
        self.ghost_ball = ghost_ball

    def aim(self):
        """Main method to handle the full aiming process."""
        self.replace_white_if_needed()
        self.update_guideline()
        self.update_cue_velocity()

    def replace_white_if_needed(self):
        """Replace the cue ball if it was pocketed last turn."""
        for ball in self.pocketed_balls.copy():
            if ball.name == 'white':
                self.pocketed_balls.remove(ball)
                self.white_ball.set_position(self.table.rect.centerx, self.cue_line.start_point[1])
                self.balls.append(self.white_ball)

    def update_guideline(self):
        """Update the guideline and ghost ball to show projected paths."""
        self.guideline.find_startpoint(self.white_ball)
        for ball in self.balls:
            ball.distance_to_white = self.white_ball.distance_to(ball)
        self.balls.sort(key=lambda b: b.distance_to_white)

        if self.settings.aiming:
            self.guideline.find_endpoint()
            self.guideline.update_white_balls_angle_attribute(self.white_ball)

        self.guideline.draw_full_line(self.balls, self.ghost_ball)
        col_ball = self.guideline.draw_ghost_ball(self.balls, self.ghost_ball)

        if self.ghost_ball.active:
            self.ghost_ball.draw()
            draw_colission_paths(self.white_ball, self.ghost_ball, col_ball, self.table, self.settings, self.screen)

    def update_cue_velocity(self):
        """Convert cue position to shot power and direction."""
        if self.settings.deciding_power:
            mouse_y = pygame.mouse.get_pos()[1]
            gf.assign_power(self.cue, mouse_y, self.white_ball, self.settings)
        self.white_ball.convert_velocity_into_x_and_y()