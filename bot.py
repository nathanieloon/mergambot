# Mergambot
# Author: Nathaniel Oon
# Date:   30/04/2016

import tictactoe

class Bot:
    def __init__(self, game):
        self.name = "Nate's Mergambot"
        self.version = "0.1.0"
        self.prog_lang = "Python"
        self.website = "http://nathanieloon.com"
        self.rpc_end_point = "http://mergambot.nathanieloon.com"
        self.desc = "Nate's Merknera Game Bot"
        self.game = game

    def status_ping(self):
        pass

    def error(self):
        pass

def main():
    ttt_game = tictactoe.Game()

if __name__ == "__main__":
    main()