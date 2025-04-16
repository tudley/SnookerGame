import pygame

class Cue():
    """ A class to model the cue.
        The cue is broken down into 3 parts, the tip, the upper body, and the lower body. This was done so ech psrt has a different colour, and looks like a real cue
        As such, moving and drawing the cue consists of interacting with each part individually, but in the methods here, all parts of the cue are evaluated at once.
    """
    def __init__(self, settings, screen):
        self.screen = screen

        # power percentage attribute
        self.percentage = "0"

        # high level dimensions of the cue
        self.cue_top = settings.cue_top
        self.cue_left = settings.cue_left
        self.cue_width = settings.cue_width
        self.cue_height = settings.cue_height

        #colour values of the cue
        self.cue_upper_body_colour = settings.cue_upper_body_colour
        self.cue_lower_body_colour = settings.cue_lower_body_colour
        self.cue_tip_colour = settings.cue_tip_colour

        # rect of the tip        
        self.cue_tip_top = self.cue_top
        self.cue_tip_height = 50
        self.cue_tip_rect = pygame.Rect(self.cue_left, self.cue_top, self.cue_width, self.cue_tip_height)

        #rect of the uppper body
        self.cue_upper_body_top = self.cue_top + self.cue_tip_height
        self.cue_upper_body_height = (2 * self.cue_height/3) - self.cue_tip_height
        self.cue_upper_body_rect = pygame.Rect(self.cue_left, self.cue_upper_body_top, self.cue_width, self.cue_upper_body_height)

        # rect of the lower body
        self.cue_lower_body_top = self.cue_top + self.cue_tip_height + self.cue_upper_body_height
        self.cue_lower_body_height = self.cue_height - (self.cue_tip_height + self.cue_upper_body_height)
        self.cue_lower_body_rect = pygame.Rect(self.cue_left, self.cue_lower_body_top, self.cue_width, self.cue_lower_body_height)

        # spacial and colour values for border around the cue
        self.border_colour = settings.border_colour
        self.divider_colour = settings.divider_colour
        self.border_top = settings.border_top
        self.border_left = settings.border_left
        self.border_width = settings.border_width
        self.border_height = settings.border_height
        self.border_rect = pygame.Rect(self.border_left, self.border_top, self.border_width, self.border_height)

        #transparent border below the cue to hide when player draws the cue back
        self.blocker_colour = settings.bg_colour
        self.blocker_left = self.border_left
        self.blocker_top = self.border_top + self.border_height
        self.blocker_height = settings.screen_height - self.blocker_top
        self.blocker_width = self.border_width
        self.blocker_rect = pygame.Rect(self.blocker_left, self.blocker_top, self.blocker_width, self.blocker_height)

    def update_rects(self):
        """This function updates the position of the cue, which will be called when the user is setting the power fo their shot"""
        self.cue_tip_top = self.cue_top
        self.cue_upper_body_top = self.cue_top + self.cue_tip_height
        self.cue_lower_body_top = self.cue_top + self.cue_tip_height + self.cue_upper_body_height

        self.cue_tip_rect = pygame.Rect(self.cue_left, self.cue_top, self.cue_width, self.cue_tip_height )
        self.cue_upper_body_rect = pygame.Rect(self.cue_left, self.cue_upper_body_top, self.cue_width, self.cue_upper_body_height)
        self.cue_lower_body_rect = pygame.Rect(self.cue_left, self.cue_lower_body_top, self.cue_width, self.cue_lower_body_height)


    def draw_cue(self):
        # draw tip
        pygame.draw.rect(self.screen, self.cue_tip_colour, self.cue_tip_rect)

        # draw upper body
        pygame.draw.rect(self.screen, self.cue_upper_body_colour, self.cue_upper_body_rect)

        # draw lower body
        pygame.draw.rect(self.screen, self.cue_lower_body_colour, self.cue_lower_body_rect)

        #draw blocker
        pygame.draw.rect(self.screen, self.blocker_colour, self.blocker_rect)

    def draw_border(self):
        """Draw a neat border around the cue, with markings per 10% power"""

        # draw border
        pygame.draw.rect(self.screen, self.border_colour, self.border_rect)

        # draw power interval markings
        for i in range(int(self.border_top + 5), int(self.border_top + 5 + self.cue_height + self.cue_height/10), int(self.cue_height/10)):
            pygame.draw.line(self.screen, self.divider_colour, (self.border_left, i), (self.border_left + self.border_width, i), 1)
       