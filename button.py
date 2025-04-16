import pygame.font

class Button():
    def __init__(self, settings, screen, text, rect):
        self.screen = screen
        self.settings = settings
        self.font = pygame.font.SysFont(None, 48)
        self.text_colour = (0, 0, 0)
        self.button_colour = (255, 255, 255)
        self.rect = rect 
        
        self.prep_msg(text)

    def prep_msg(self, text):
        """Turn a msg into a rendered image and center text on the button"""
        self.msg_image = self.font.render(text, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """draw blank button and then draw message"""
        self.screen.fill(self.button_colour, self.msg_image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
    


class Choice_button(Button):
    def __init__(self, settings, screen, text, rect):
        super().__init__(settings, screen, text, rect)

    def draw_choice_button(self):
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        self.screen.fill(self.button_colour, self.msg_image_rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

        # draw the rects for player to chose red or yellow team
        pygame.draw.circle(self.screen, self.settings.red_ball_col, self.settings.red_ball_center, self.settings.ball_radius * 2)
        pygame.draw.circle(self.screen, self.settings.yellow_ball_col, self.settings.yellow_ball_center, self.settings.ball_radius * 2)

