# Bot superclass for Mergambot
# Author: Nathaniel Oon
# Date:   03/05/2016

class Bot:
    def __init__(self, game):
        self.game = game

    def get_game(self):
        return self.game