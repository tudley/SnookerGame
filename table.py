import pygame

class Table():
    """A class to model the table, purely for aesthetics and a reference to position all other parts of a pool table to"""
    def __init__(self, settings, screen):
        #initialise attributes
        self.screen = screen
        self.width = settings.table_width
        self.left = settings.table_left
        self.top = settings.table_top
        self.height = settings.table_height
        self.colour = settings.table_colour
        self.rect = pygame.Rect(self.left, self.top, self.width, self.height)
    
    def draw_table(self):
        """Draw the table to the screen"""
        pygame.draw.rect(self.screen, self.colour, self.rect)