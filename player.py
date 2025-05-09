
class Player():
    """A simple class to model a player. This is where you store the 'meta' attributes of a player, their team, advantage ect."""
    def __init__(self, name):
        self.name = name
        self.team = None
        self.foul1 = False
        self.foul2 = False
        self.foul3 = False
        self.foul4 = False
        self.fouls = [self.foul1, self.foul2, self.foul3, self.foul4]
        self.gameover = False
        self.advantage = False
        self.win = False
