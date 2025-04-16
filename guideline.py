import pygame
import math

class Guideline():
    def __init__(self, settings, screen, cue_ball, table):

        self.width = settings.guideline_width
        self.colour = settings.line_colour
        self.screen = screen
        self.table = table
        self.settings = settings
        self.coliding_ball = None


        self.startpoint_x, self.startpoint_y = cue_ball.centerx, cue_ball.centery
        self.startpoint = (self.startpoint_x, self.startpoint_y)
        self.mousepoint_x, self.mousepoint_y = 0, 0
        self.gradient = (self.mousepoint_y - self.startpoint_y) / (self.mousepoint_x - self.startpoint_x)
        self.c = self.startpoint_y - (self.gradient * self.startpoint_x)

    def find_startpoint(self, cue_ball):
        self.startpoint_x, self.startpoint_y = cue_ball.centerx, cue_ball.centery
        self.startpoint = (self.startpoint_x, self.startpoint_y)

    def find_endpoint(self):
        self.mousepoint_x, self.mousepoint_y = pygame.mouse.get_pos()
        self.mousepoint = self.mousepoint_x, self.mousepoint_y
        try:
            self.gradient = (self.mousepoint_y - self.startpoint_y) / (self.mousepoint_x - self.startpoint_x)
        except:
            self.gradient = 10**10
        self.c = self.startpoint_y - (self.gradient * self.startpoint_x)

    def draw_full_line(self, balls, ghost_ball):
        """Draw a black line from the center of the white ball passing through the cursor"""

        #set generic endpoints until user begins aiming
        self.endpoint_x = self.table.rect.centerx
        self.endpoint_y = self.table.rect.centery

        #if player is aiming to the right
        if self.mousepoint_x > self.startpoint_x:
            # set the x endpoint at the cushion boundary
            self.endpoint_x = self.table.rect.right - self.settings.cushion_width
            self.endpoint_y = self.gradient * self.endpoint_x + self.c
            # if the y position is above the bounds of the table, set the y endpoint as the top cushion boundary
            if self.endpoint_y < self.table.rect.top + self.settings.cushion_width:
                #print('top edge')
                self.endpoint_y = self.table.rect.top + self.settings.cushion_width
                self.endpoint_x = (self.endpoint_y - self.c) / self.gradient
            # if the y position is below the bounds of the table, set the y endpoint as the bottom cushion boundary
            elif self.endpoint_y > self.table.rect.bottom - self.settings.cushion_width:
                #print('bot edge')
                self.endpoint_y = self.table.rect.bottom - self.settings.cushion_width
                self.endpoint_x = (self.endpoint_y - self.c) / self.gradient

        #if player is eiming to the left/vertical
        elif self.mousepoint_x <= self.startpoint_x:
            self.endpoint_x = self.table.rect.left + self.settings.cushion_width
            self.endpoint_y = self.gradient * self.endpoint_x + self.c
            if self.endpoint_y < self.table.rect.top + self.settings.cushion_width:
                #print('top edge')
                self.endpoint_y = self.table.rect.top + self.settings.cushion_width
                self.endpoint_x = (self.endpoint_y - self.c) / self.gradient
            
            elif self.endpoint_y > self.table.rect.bottom - self.settings.cushion_width:
                #print('bot edge')
                self.endpoint_y = self.table.rect.bottom - self.settings.cushion_width
                self.endpoint_x = (self.endpoint_y - self.c) / self.gradient
        self.endpoint = (self.endpoint_x, self.endpoint_y)

        if ghost_ball.active == True:
            self.endpoint = (ghost_ball.centerx, ghost_ball.centery)

        pygame.draw.line(self.screen, (0, 0, 0), self.startpoint, self.endpoint, 3)

    def draw_ghost_ball(self, balls, ghost_ball):

        # draw the 'ghost ball' where the guidline meets the closest ball     
        ghost_ball.active = False   
        for ball in balls:
            if ball.name != 'white':
                
                # if player is aiming to the right
                if self.mousepoint_x > self.startpoint_x:
                    # create a circle at a regular interval at each point on the guidline
                    for x in range(int(self.startpoint_x), int(self.endpoint_x), 1):
                        y = (self.gradient * x) + self.c
                        c1 = (x, y)
                        c2 = (ball.centerx, ball.centery)
                        # find the distance between the point and the center of the circle
                        c1c2 = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
                        # evaluate if the value is less than or equal to 2 * the radius of the ball,
                        # meaning this is where the cue ball strikes the ball
                        if c1c2 <= (2* ball.radius):
                            # draw the ghost ball at this point
                            ghost_ball.centerx, ghost_ball.centery = c1
                            ghost_ball.active = True
                            coliding_ball = ball
                            #print(ball.name)
                            break
                        else:
                            ghost_ball.active = False


                elif self.mousepoint_x <= self.startpoint_x:
                    for x in range(int(self.startpoint_x), int(self.endpoint_x), -1):
                        y = (self.gradient * x) + self.c
                        c1 = (x, y)
                        c2 = (ball.centerx, ball.centery)
                        c1c2 = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

                        if c1c2 <= (2* ball.radius) * 1:
                            ghost_ball.centerx, ghost_ball.centery = c1
                            ghost_ball.active = True
                            coliding_ball = ball
                            break
            if ghost_ball.active == True:
                return coliding_ball

        
    def update_white_balls_angle_attribute(self, cue_ball):
        """adjust the white balls 'theta' attribute based on mouse position whilst aiming to later convert velocity magnitude to x and y components"""
        delta_y = self.mousepoint_y - self.startpoint_y
        delta_x = self.mousepoint_x - self.startpoint_x

        cue_ball.theta = math.atan2(delta_y, delta_x)
