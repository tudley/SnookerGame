import pygame
from pygame.sprite import Sprite
import math
from triangle_collision import find_collision, calc_new_speeds, find_nearest_triangle
import restitution_2 as res2

class Ball(Sprite):
    """A class to model a pool ball"""
    def __init__(self, settings, screen, colour, mass=1, ghost=False):
        super().__init__()

        #attributes of the ball
        self.screen = screen
        self.settings = settings
        self.radius = settings.ball_radius
        self.colour = colour
        self.mass = mass
        self.e = 1
        #self.name = 'cue'
        self.ghost = ghost
        self.distance_to_white = 0

        # declare balls 'name' based on its colour value
        if colour == settings.red_ball_col:
            self.name = 'red'
        if colour == settings.black_ball_col:
            self.name = 'black'
        if colour == settings.yellow_ball_col:
            self.name = 'yellow'
        if colour == settings.cue_ball_col:
            self.name = 'white'
            
        #ghost ball settings
        self.active = False

        #speed flags
        self.x_vel = 0
        self.y_vel = 0
        self.v_mag = 0
        # angle of velocity vector
        try:
            self.theta = math.atan2(self.y_vel/self.x_vel)
        except:
            # if x_vel == 0, theta = 90 degrees
            self.theta = math.radians(90)

        # coordinates of the ball
        self.centerx = settings.screen_width/2
        self.centery = settings.screen_height/2

        #set attributes for the corners of the ball
        # Use a loop from -pi to pi, and each increment, create a 'corner' point for the hitbox of the ball
        
        self.corners = {}
        for phi in range(-16, 16, 1):
            num = phi/16
            phi *= math.pi / 32
            corner = (self.centerx + self.radius * math.cos(phi), self.centery + self.radius * math.sin(phi))
            self.corners[num] = (corner)

        
    def set_position(self, x, y):
        self.centerx = x
        self.centery = y
        
    def distance_to(self, other):
        distance = math.sqrt((self.centerx - other.centerx)**2 + (self.centerx - other.centerx)**2)
        return distance

    def draw(self):
        """Draw the ball to the screen"""
        pygame.draw.circle(self.screen, self.colour, (self.centerx, self.centery), self.radius)

        # if ball is the 'ghost ball', draw it 'hollow'
        if self.ghost == True:
            pygame.draw.circle(self.screen, self.colour, (self.centerx, self.centery), self.radius)
            pygame.draw.circle(self.screen, self.settings.table_colour, (self.centerx, self.centery), self.radius * 0.9)


    def convert_velocity_into_x_and_y(self):
        "Using the magnitude of the balls velocity, and the angle its travelling at, convert it into x and y components"
        self.x_vel = self.v_mag * math.cos(self.theta)
        self.y_vel = self.v_mag * math.sin(self.theta)

    def update_ball_position(self):
        """Move the balls coordinates based on its velocity"""
        # update the centers
        self.centerx += self.x_vel
        self.centery += self.y_vel
        self.centerx = float(self.centerx)
        self.centery = float(self.centery)

        # update the corners
        for phi in range(-16, 16, 1):
            num = phi/16
            phi *= math.pi / 32
            corner = (self.centerx + self.radius * math.cos(phi), self.centery + self.radius * math.sin(phi))
            self.corners[num] = (corner)

    def apply_friction(self):
        """reduce the speed of the balls to model friction"""
        friction = 0.994
        self.x_vel = self.x_vel * friction if abs(self.x_vel) > 0.1 else 0
        self.y_vel = self.y_vel * friction if abs(self.y_vel) > 0.1 else 0

    def check_wall_collission(self, cushions):
        """check if a ball hits the edge of the table, and adjust the balls velocity appropriately"""
        
        # Here we define the balls right, left, top and bottom edges clearly
        self.r_edge = self.centerx + self.radius
        self.l_edge = self.centerx - self.radius
        self.t_edge = self.centery - self.radius
        self.b_edge = self.centery + self.radius

        # Now we check each cushion on the table, checking if the ball has collided with it
        # And if it has, we reverse the appropriate velocity component
        for cushion in cushions:
            if cushion.side == 'left':
                if self.centery < cushion.rect.bottom and self.centery > cushion.rect.top:
                    if self.l_edge <= cushion.rect.right:
                        self.x_vel *= -1
            
            if cushion.side == 'right':
                if self.centery < cushion.rect.bottom and self.centery > cushion.rect.top:
                    if self.r_edge >= cushion.rect.left:
                        self.x_vel *= -1
            
            if cushion.side == 'top':
                if self.centerx < cushion.rect.right and self.centerx > cushion.rect.left:
                    if self.t_edge <= cushion.rect.bottom:
                        self.y_vel *= -1
            
            if cushion.side == 'bot':
                if self.centerx < cushion.rect.right and self.centerx > cushion.rect.left:
                    if self.b_edge >= cushion.rect.top:
                        self.y_vel *= -1

    def check_triangle_collission(self, triangles):
        """Check if a ball collides with the triangluar edge of the cushion"""
        # This function requires a lot of computation, so to optimise it, we first identify the nearest triangle to focus on.
        nearest_triangle = find_nearest_triangle(self, triangles)
        if find_collision(nearest_triangle, self):
            calc_new_speeds(self, nearest_triangle)

    def check_collission_with_ball(self, other, settings):
        """Check if the distance between the ball and another ball are smaller than the sum of their radii
           If it is, balls have 'collided' and funct will return True"""
        dist_between_centers = math.sqrt((self.centerx - other.centerx)**2 + (self.centery - other.centery)**2)
        if dist_between_centers <= self.radius + other.radius:
            if settings.first_contact == None:
                settings.first_contact = other.name
            return True
        
    def resolve_collission_with(self, other, settings):
        """Use coefficient of restitution to calculate and apply post collission velocities to 'host' ball and interacting ball"""
        res2.apply_collission_and_find_new_speeds(self, other, settings)





