# Tic Tac Toe module for Mergambot
# Author: Nathaniel Oon
# Date:   30/04/2016

from bot import Bot
import random, requests, json

class TicTacToeBot(Bot):
    """ Tic Tac Toe Bot class
    """
    def __init__(self, game_id, mark):
        """ Initialise bot
        """
        Bot.__init__(self, 'TICTACTOE')
        self.game_id = gameid
        self.mark = mark
        self.game_state = 'BEGIN'

    def status_ping(self):
        """ Ping ping
        """
        pass

    def next_move(self, board):
        """ Function for taking the next move
        """
        # Choose a random tile
        choice = random.randint(0,8)

        # Get an empty tile
        while board.board_tiles[choice] is not None:
            choice = random.randint(0,8)

        # Fill a tile
        board.board_tiles[choice] = self.mark

    def complete(self):
        """ Function for handling the complete state
        """
        self.game_state = "COMPLETE"

    def error(self):
        """ Error "handling"
        """
        pass

class Board:
    def __init__(self):
        """ Define the board for Tic Tac Toe
        """
        self.board_tiles = [None, None, None,
                            None, None, None,
                            None, None, None]

    def print_board(self):
        """ Helper function for printing out the current board state
        """
        # Space it out a bit
        # TODO: Put information about turns here?
        print ""

        # Print the board
        for i, tile in enumerate(self.board_tiles):
            # Use a blank space for empty tiles
            if tile == None:
                    tile = '-'

            # Print the board
            if i == 8:
                print str(tile)
            elif (i+1) % 3 == 0:
                print str(tile)
                print "---------"
            else:
                print str(tile) + " |",


class Game:
    def __init__(self):
        board = Board()
        board.print_board()

        bot = TicTacToeBot(1, "X")
        bot.next_move(board)
        board.print_board()