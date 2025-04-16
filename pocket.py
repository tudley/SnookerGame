import pygame
import math

class Pocket():
    """A class modelling the pockets of a pool table, they will cause a ball to 'dissapear' if all the balls edges lie within the pocket radius"""
    def __init__(self, settings, screen, table, position):
        #initialise the attributes
        self.screen = screen
        self.radius = settings.pocket_radius
        self.colour = settings.pocket_colour
        self.table = table
        self.position = position
        #create a variable to postition the corner pockets better
        self.corner_pocket_adjustment = (self.radius * math.sqrt(2)) / 4

        #defite the center pos the pocket based on which pocket it is
        if position == 'topleft':
            self.centerx = self.table.rect.left + self.corner_pocket_adjustment
            self.centery = self.table.rect.top + self.corner_pocket_adjustment
            self.name = position

        if position == 'topright':
            self.centerx = self.table.rect.right - self.corner_pocket_adjustment
            self.centery = self.table.rect.top + self.corner_pocket_adjustment

        if position == 'midright':
            self.centerx = self.table.rect.right - self.corner_pocket_adjustment
            self.centery = self.table.rect.centery

        if position == 'midleft':
            self.centerx = self.table.rect.left + self.corner_pocket_adjustment
            self.centery = self.table.rect.centery

        if position == 'botright':
            self.centerx = self.table.rect.right - self.corner_pocket_adjustment
            self.centery = self.table.rect.bottom - self.corner_pocket_adjustment
            
        if position == 'botleft':
            self.centerx = self.table.rect.left + self.corner_pocket_adjustment
            self.centery = self.table.rect.bottom - self.corner_pocket_adjustment

    def draw_pocket(self):
        """Draw the pocket to the screen""" 
        pygame.draw.circle(self.screen, self.colour, (self.centerx, self.centery), self.radius)



