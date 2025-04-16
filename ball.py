import pygame
from pygame.sprite import Sprite
import math

class Ball(Sprite):
    """A class to model a pool ball"""
    def __init__(self, settings, screen, colour, mass=1, ghost = False):
        super().__init__()

        #attributes of the ball
        self.screen = screen
        self.settings = settings
        self.radius = settings.ball_radius
        self.colour = colour
        self.mass = mass
        self.e = 1
        self.name = 'cue'
        self.ghost = ghost
        self.distance_to_white = 0

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
        #center the ball
        self.centerx = settings.screen_width/2
        self.centery = settings.screen_height/2

        #set attributes for the corners of the ball


        # ATTEMPT 1: Use a loop from -pi to pi, and each increment, create a 'corner' point for the hitbox of the ball
        self.corners = {}
        for phi in range(-16, 16, 1):
            num = phi/16
            phi *= math.pi / 32
            corner = (self.centerx + self.radius * math.cos(phi), self.centery + self.radius * math.sin(phi))
            self.corners[num] = (corner)

        
        # ATTEMPT 2: Currently legacied. corners are manually set, TopRight, TopLeft, BottomRight, BottomLeft
        """        
        self.phi = math.pi / 4

        self.tl = (self.centerx - self.radius * math.sin(self.phi), self.centery - self.radius * math.sin(self.phi))
        self.tr = (self.centerx + self.radius * math.sin(self.phi), self.centery - self.radius * math.sin(self.phi))
        self.bl = (self.centerx - self.radius * math.sin(self.phi), self.centery + self.radius * math.sin(self.phi))
        self.br = (self.centerx + self.radius * math.sin(self.phi), self.centery + self.radius * math.sin(self.phi))

        self.corners = {'tl': self.tl, 'tr' : self.tr, 'bl' : self.br, 'br' : self.br}
        """
        
    def draw(self):
        """Draw the ball to the screen"""
        pygame.draw.circle(self.screen, self.colour, (self.centerx, self.centery), self.radius)

        if self.ghost == True:
            pygame.draw.circle(self.screen, self.colour, (self.centerx, self.centery), self.radius)
            pygame.draw.circle(self.screen, self.settings.table_colour, (self.centerx, self.centery), self.radius * 0.9)


    def convert_velocity_into_x_and_y(self):
        "Using the magnitude of the balls velocity, and the angle its travelling at, convert it into x and y components"
        self.x_vel = self.v_mag * math.cos(self.theta)
        self.y_vel = self.v_mag * math.sin(self.theta)

