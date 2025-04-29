

def auto_assign_teams(settings):
    """Auto assigns both players a team based on the colour of the ball pocketed"""
    settings.active_player.team = settings.balls_pocketed_in_turn[0].name
    if settings.balls_pocketed_in_turn[0].name == 'yellow':
        settings.inactive_player.team = 'red'
    else:
        settings.inactive_player.team = 'yellow'

def assign_teams(settings, choice_button2, choice_button):
    """Player has the ability to chose their team from potting 2 differrent colours"""
    settings.player_chose_team = True
    choice_button2.draw_choice_button() 
    choice_button.draw_button() 

def check_gameover(settings):
    """Player on the black pots another ball with it"""
    if settings.active_player.team == 'black':
        for ball in settings.balls_pocketed_in_turn:
            if ball.name == 'black':
                settings.gameover = True

def end_evaluation(settings):
    """Ends the 'evaluation' phase of the game, reactivates the 'deciding shot' phase"""
    settings.evaluating_shot = False
    settings.deciding_shot = True
    settings.first_contact = None
    for ball in settings.balls_pocketed_in_turn.copy():
        settings.balls_pocketed_in_turn.remove(ball)

def give_advantage(settings):
    """Give the inactive player the advantage"""
    settings.inactive_player.advantage = True

def swap_active_player(players, settings):
    if settings.active_player == players[0]:
        settings.active_player = players[1]
        settings.inactive_player = players[0]
    elif settings.active_player == players[1]:
        settings.active_player = players[0]
        settings.inactive_player = players[1]

def check_foul1(settings):
    """check if player pots the white ball"""
    for ball in settings.balls_pocketed_in_turn:
        #print(ball.name)
        if ball.name == "white":
            settings.active_player.foul1 = True
            print(settings.active_player.name, ' has potted the white')

def check_foul2(settings):
    """check if the player hits the opponents ball first"""
    if settings.first_contact == settings.inactive_player.team:
        settings.active_player.foul2 = True
        print(settings.active_player.name, ' has hit the opponents ball first')
        return True
    else:
        return False

def check_foul3(settings):
    """check if the player pockets an opponents ball"""
    colours = set(ball.name for ball in settings.balls_pocketed_in_turn)
    if settings.inactive_player.team in colours:
        settings.active_player.foul3 = True
        print(settings.active_player.name, 'has pocketed their opponents ball')


def check_foul4(settings):
    if settings.first_contact == None:
        settings.active_player.foul4 = True
        print(settings.active_player.name, ' did not make contact with any balls')
        return True
    else:
        return False
    
def check_if_player_has_potted_all_their_balls(settings, balls):
    """assigns a player to team 'black' if the pot all their colour balls"""
    remaining_team_balls = 0
    for ball in balls:
        if ball.name == settings.active_player.team:
            remaining_team_balls += 1
    if remaining_team_balls == 0:
        print('player has potted all their balls and now needs to pot the black')
        settings.active_player.team = 'black'

def check_for_win(settings):
    if settings.active_player.team == 'black':
        if settings.active_player.foul1 == False and settings.active_player.foul2 == False and settings.active_player.foul3 == False:
            if len(settings.balls_pocketed_in_turn) == 1:
                if settings.balls_pocketed_in_turn[0].name == 'black':
                    settings.active_player.win = True
                    print(f"{settings.active_player.name} has won the game")