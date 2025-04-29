import pygame

class Settings():
    def __init__(self):

        #screen settings
        self.screen_height = 800
        self.screen_width = (self.screen_height + 400) / 2
        self.screen_gradient = self.screen_height / self.screen_width
        self.bg_colour = (150, 150, 150)

        #table settings
        self.table_height = self.screen_height - 100
        self.table_width = self.table_height * (48 / 92)
        self.table_left = 50
        self.table_top = 50
        self.table_colour = (10, 108, 3)

        #ball settings
        self.ball_radius = self.table_height * 2.25 / 100
        self.cue_ball_col = (255, 255, 240)
        self.red_ball_col = (125, 20, 35)
        self.yellow_ball_col = (252, 222, 12)
        self.black_ball_col = (0, 0, 0)
        self.green_ball_col = (10, 220, 30)
        self.max_speed = 10

        #rail settings
        self.rail_colour = (142, 84, 35)

        #pocket settings
        #self.pocket_radius = self.table_height * (4.5 / 92)
        self.pocket_radius = self.ball_radius * 2
        self.pocket_colour = (0, 0, 0)

        #cushion settings
        self.cushion_colour = (9, 89, 12)
        self.cushion_width = 2 * self.table_height / 92

        #line settings
        self.line_colour = (255, 255, 255)
        self.line_width = 2
        self.guideline_width = self.ball_radius

        # shoot button settings
        self.shoot_button_colour = (200, 0, 0)
        self.shoot_button_top = self.table_top + self.table_height
        self.shoot_button_left = self.table_left + self.table_width + self.pocket_radius
        self.shoot_button_width = 100
        self.shoot_button_height = 50
        self.shoot_rect = pygame.Rect(self.shoot_button_left, self.shoot_button_top, self.shoot_button_width, self.shoot_button_height)

        #gamestate settings
        self.deciding_shot = True
        self.aiming = False
        self.moving_balls = False
        self.evaluating_shot = False
        self.deciding_power = False
        self.turn = 1
        self.first_contact = None
        self.balls_pocketed_in_turn = []
        self.player_chose_team = False

        # player settings
        self.player_rect = pygame.Rect(self.table_left, self.table_top - self.pocket_radius, 500, self.pocket_radius)
        self.active_player = None
        self.inactive_player = None

        # side cue and border settings
        self.border_colour = (255, 0, 0)
        self.divider_colour = (0, 0, 0)
        self.border_top = 50
        self.border_left = self.table_left + self.table_width + 50
        self.border_width = 30
        self.border_height = self.screen_height - 100

        self.cue_lower_body_colour = (80, 24, 11)
        self.cue_upper_body_colour = (205, 148, 92)
        self.cue_tip_colour = (255, 255, 255)
        self.cue_top = self.border_top + 5
        self.cue_left = self.border_left + 5
        self.cue_width = self.border_width - 10
        self.cue_height = self.border_height - 10

        # percetnage button dimenssions
        self.percentage_colour = self.shoot_button_colour
        self.percentage_left = self.table_left + self.table_width + 2 * self.ball_radius + 10
        self.percentage_height = self.border_top
        self.percentage_top = self.border_top - self.percentage_height
        self.percentage_width = 50
        self.percentage_rect = pygame.Rect(self.percentage_left, self.percentage_top, self.percentage_width, self.percentage_height)
        
        # choice button dimensions
        self.choice_left = self.table_left
        self.choice_top = self.table_top + self.table_height/2
        self.choice2_top = self.choice_top + 30
        self.choice_width = self.table_width + self.ball_radius
        self.choice_height = 100
        self.choice_colour_width = self.table_width / 3

        self.choice1_rect = pygame.Rect(self.choice_left, self.choice_top, self.choice_width, self.choice_height)
        self.choice2_rect = pygame.Rect(self.choice_left, self.choice2_top, self.choice_width, self.choice_height)
        self.red_ball_center = ((self.choice_left + 2 * self.ball_radius + 10), (self.choice2_top + self.choice_height - self.ball_radius))
        self.yellow_ball_center = (((self.choice_left + self.choice_width - 10 - 2 * self.ball_radius), self.choice2_top + self.choice_height - self.ball_radius))

