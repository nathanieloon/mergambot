# Tic Tac Toe module for Mergambot
# Author: Nathaniel Oon
# Date:   30/04/2016

from bot import Bot
import random

class TicTacToeBot(Bot):
    """ Tic Tac Toe Bot class
    """
    def __init__(self):
        """ Initialise bot
        """
        Bot.__init__(self, 'TICTACTOE')
        self.game_id = None
        self.mark = None
        self.game_status = None
        self.board = Board()

    def make_move(self, gameid, mark, gamestate):
        """ Function for taking the next move
        """
        # Set our mark and id if we haven't got one
        if self.mark is None:
            self.mark = mark
        if self.game_id is None:
            self.game_id = gameid
        if self.game_status is None or  self.game_status is 'COMPLETE':
            self.game_status = 'PLAYING'

        # Update the board
        self.board.update_board(gamestate)

        # Decide and make our move
        move = self.next_move()

        # Show the board
        self.board.print_board()

        #Return move
        response = {'position': move}
        return response

    def complete(self, gameid, winner, mark, gamestate):
        """ Function for handling the complete state
        """
        self.game_status = 'COMPLETE'
        # Print results of the game
        print "======= Game is complete ======="
        print "Game ID: ", gameid
        if winner is True:
            winna = "Us :D"
        else:
            winna = "Them :("
        print "Winner: ", winna

        # Update and print the board
        self.board.update_board(gamestate)
        print "Board: "
        self.board.print_board()

        response = {'status': 'OK'}
        return response

    def error_message(self, gameid, message, errorcode):
        """ Error message handling
        """
        self.game_status = 'ERROR'
        print "Merknera: Error in game_id:", gameid, ",", message, ", Error code:", errorcode

        response = {'status': 'OK'}
        return response 

    def next_move(self):
        """ Function for determining the next move to be played

            Currently very simple, just taking an empty, random tile
        """
        # Choose a random tile
        move = random.randint(0,8)

        # Get an empty tile
        while self.board.get_tile(move) is not None:
            move = random.randint(0,8)

        # Fill a tile
        self.board.assign_move(move, self.mark)

        return move

    def get_game_status(self):
        """ Helper function to get the game state
        """
        return self.game_status

class Board:
    def __init__(self):
        """ Define the board for Tic Tac Toe
        """
        self.board_tiles = [None, None, None,
                            None, None, None,
                            None, None, None]

    def update_board(self, game_state):
        """ Update the board with a specific game state
        """
        for i, tile in enumerate(game_state):
            self.assign_move(i, tile)

    def assign_move(self, tile, mark):
        """ Assign a move on the board with the given tile and mark
        """
        # Replace blank strings with None
        if mark == "":
            mark = None

        # Update tile
        self.board_tiles[tile] = mark

    def get_tile(self, tile):
        """ Get the given tile
        """
        return self.board_tiles[tile]

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
