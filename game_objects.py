import pygame

class Rail():
    """a class to model the wooden sides of the pool table, purely for aesthetics"""
    def __init__(self, settings, screen, table, pocket):
        #initialise attributes
        self.screen = screen
        self.settings = settings
        self.table = table
        self.pocket = pocket
        self.colour = settings.rail_colour
        self.thickness = pocket.radius

        #definte the positions of the rails
        self.wide_rect = pygame.Rect(self.table.rect.left - self.thickness, self.table.rect.top, self.table.rect.width + (2 * self.thickness), self.table.rect.height)
        self.tall_rect = pygame.Rect(self.table.rect.left, self.table.rect.top - self.thickness, self.table.rect.width, self.table.rect.height + (2 * self.thickness))

    def draw_rail(self):
        """draw the rails to the screen"""
        #pygame.draw.rect(self.screen, self.colour, self.rect)
        pygame.draw.rect(self.screen, self.colour, self.tall_rect)
        pygame.draw.rect(self.screen, self.colour, self.wide_rect)
        pygame.draw.circle(self.screen, self.colour, (self.table.rect.topleft), self.thickness)
        pygame.draw.circle(self.screen, self.colour, (self.table.rect.topright), self.thickness)
        pygame.draw.circle(self.screen, self.colour, (self.table.rect.bottomleft), self.thickness)
        pygame.draw.circle(self.screen, self.colour, (self.table.rect.bottomright), self.thickness)


class Cushion():
    """A class to model the cushions of the pool table, they will deal with colissions with balls"""
    def __init__(self, settings, screen, table, pocket1, side, position, pocket2):
        #initialise attributes
        self.screen = screen
        self.settings = settings
        self.table = table
        self.pocket1 = pocket1
        self.pocket2 = pocket2
        #self.colour = (142, 84, 35)
        self.colour = settings.cushion_colour
        self.side = side
        self.cushion_width = settings.cushion_width
        self.angle_colour = (10, 108, 3)

        # definte the rects of the cushions based on the position on the table
        if position == 'top':
            self.rect = pygame.Rect(self.table.rect.left + self.pocket1.radius + self.cushion_width + pocket1.corner_pocket_adjustment, self.table.rect.top, self.table.rect.width - 2 * (self.pocket1.radius + self.cushion_width + self.pocket1.corner_pocket_adjustment) + 1, self.cushion_width + 1)
        
        if position == 'topleft':
            self.rect = pygame.Rect(self.table.rect.left, pocket1.centery + self.pocket1.radius + self.cushion_width, self.cushion_width + 1, (pocket2.centery - pocket2.radius - self.cushion_width) - (pocket1.centery + self.pocket1.radius + self.cushion_width))
        
        if position == 'topright':
            self.rect = pygame.Rect(self.table.rect.right - self.cushion_width, pocket1.centery + self.pocket1.radius + self.cushion_width, self.cushion_width + 1, (pocket2.centery - pocket2.radius - self.cushion_width) - (pocket1.centery + self.pocket1.radius + self.cushion_width))
        
        if position == 'botleft':
            self.rect = pygame.Rect(self.table.rect.left, pocket1.centery + self.pocket1.radius + self.cushion_width, self.cushion_width + 1, (pocket2.centery - pocket2.radius - self.cushion_width) - (pocket1.centery + self.pocket1.radius + self.cushion_width))
        
        if position == 'botright':
            self.rect = pygame.Rect(self.table.rect.right - self.cushion_width, pocket1.centery + self.pocket1.radius + self.cushion_width, self.cushion_width + 1, (pocket2.centery - pocket2.radius - self.cushion_width) - (pocket1.centery + self.pocket1.radius + self.cushion_width))
        
        if position == 'bot':
            self.rect = pygame.Rect(self.table.rect.left + self.pocket1.radius + self.cushion_width + pocket1.corner_pocket_adjustment, self.table.rect.bottom - self.cushion_width, self.table.rect.width - 2 * (self.pocket1.radius + self.cushion_width + self.pocket1.corner_pocket_adjustment) + 1, self.cushion_width + 1)
       
    def draw_cushion(self):
        """Draw the cushion to the screen"""
        
        pygame.draw.rect(self.screen, self.colour, self.rect)

class Triangle():
    def __init__(self, position, table, pocket, settings, screen):
        #x3 and y3 are the edges of the triangle we never touch

        self.colour = settings.cushion_colour
        self.screen = screen
        self.width = settings.cushion_width

        if position == 'topleft top':
            self.x1, self.y1 = table.rect.left, pocket.centery + pocket.radius
            self.x2, self.y2 = table.rect.left + self.width, pocket.centery + pocket.radius + self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'top left':
            self.x1, self.y1 =  pocket.centerx + pocket.radius + self.width, table.rect.top + self.width
            self.x2, self.y2 = pocket.centerx + pocket.radius, table.rect.top
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'top right':
            self.x1, self.y1 = pocket.centerx - pocket.radius - self.width, table.rect.top + self.width
            self.x2, self.y2 = pocket.centerx - pocket.radius, table.rect.top
            self.x3, self.y3 =  self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'topright top':
            self.x1, self.y1 = table.rect.right - 1, pocket.centery + pocket.radius
            self.x2, self.y2 = table.rect.right - self.width, pocket.centery + pocket.radius + self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))
                   
        if position == 'topleft bot':
            self.x1, self.y1 = table.rect.left, pocket.centery - pocket.radius
            self.x2, self.y2 = table.rect.left + self.width, pocket.centery - pocket.radius - self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3)) 
        
        if position == 'topright bot':
            self.x1, self.y1 = table.rect.right - 1, pocket.centery - pocket.radius
            self.x2, self.y2 = table.rect.right - self.width, pocket.centery - pocket.radius - self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))  

        if position == 'botleft top':
            self.x1, self.y1 = table.rect.left, pocket.centery + pocket.radius
            self.x2, self.y2 = table.rect.left + self.width, pocket.centery + pocket.radius + self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))   

        if position == 'botright top':
            self.x1, self.y1 = table.rect.right - 1, pocket.centery + pocket.radius
            self.x2, self.y2 = table.rect.right - self.width, pocket.centery + pocket.radius + self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'botleft bot':
            self.x1, self.y1 = table.rect.left, pocket.centery - pocket.radius
            self.x2, self.y2 = table.rect.left + self.width, pocket.centery - pocket.radius - self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'botright bot':
            self.x1, self.y1 = table.rect.right - 1, pocket.centery - pocket.radius
            self.x2, self.y2 = table.rect.right - self.width, pocket.centery - pocket.radius - self.width
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))

        if position == 'bot left':
            self.x1, self.y1 = pocket.centerx + pocket.radius + self.width, table.rect.bottom - self.width
            self.x2, self.y2 = pocket.centerx + pocket.radius, table.rect.bottom -1
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))


        if position == 'bot right':
            self.x1, self.y1 = pocket.centerx - pocket.radius - self.width, table.rect.bottom - self.width
            self.x2, self.y2 = pocket.centerx - pocket.radius, table.rect.bottom -1
            self.x3, self.y3 = self.x1, self.y2
            self.triangle = ((self.x1, self.y1), (self.x2, self.y2), (self.x3, self.y3))




    def draw_triangle(self):
        pygame.draw.polygon(self.screen, self.colour, self.triangle)

class Pocket_hitbox():
    """A class to model a hitbox behind a pocket in case the ball passes the pocket without registering a hit"""
    def __init__(self, settings, screen, pocket):
        self.settings = settings
        self.screen = screen
        self.colour = (50, 50, 50)
        self.centerx = pocket.centerx
        self.centery = pocket.centery
        self.width = 2 * pocket.radius
        self.rect = pygame.Rect((self.centerx - self.width / 2), (self.centery - self.width / 2), self.width, self.width)

    def draw_hitbox(self):
        pygame.draw.rect(self.screen, self.colour, self.rect)


class Line():
    def __init__(self, position, settings, screen, table):
        self.screen = screen
        self.colour = settings.line_colour
        self.width = settings.line_width
        if position == 'cue line':
            self.start_point = (table.rect.left, table.rect.bottom - table.rect.height/4)
            self.end_point = (table.rect.right - 1, table.rect.bottom - table.rect.height/4)

        if position == 'black spot':
            self.start_point = (table.rect.left, table.rect.bottom - 3 * table.rect.height/4)
            self.end_point = (table.rect.right - 1, table.rect.bottom - 3 * table.rect.height/4)
        
    def draw_line(self):
        pygame.draw.line(self.screen, self.colour, self.start_point, self.end_point, self.width)