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
        # self.game_status = None
        self.board = Board()

    def make_move(self, gameid, mark, gamestate, opponent):
        """ Function for taking the next move
        """
        # Set our mark and id for this turn
        # Note: This is kinda weird, because of multiple games. 
        # Think of it as mark and id the bot is focusing on for this particular turn.
        self.mark = mark
        self.game_id = gameid
        # if self.game_status is None or  self.game_status is 'COMPLETE':
        #     self.game_status = 'PLAYING'

        # Update the board
        self.board.update_board(gamestate)

        # Decide and make our move
        move = self.next_move()

        # Show the board
        self.board.print_board(gameid, mark)

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
            winna = "We win!"
        else:
            winna = "Tie or loss"
        print "Winner: ", winna

        # Update and print the board
        self.board.update_board(gamestate)
        print "Board: "
        self.board.print_board(gameid, mark)

        response = {'status': 'OK'}
        return response

    def error_message(self, gameid, message, errorcode):
        """ Error message handling
        """
        self.game_status = 'ERROR'
        print "Merknera: Error in game_id: {0}, {1}, Error code: {2}".format(gameid, message, errorcode)

        response = {'status': 'OK'}
        return response 

    def next_move(self):
        """ Function for determining the next move to be played
        """
        board = self.board.board_tiles
        board_len = self.board.board_len
        empty_tiles = self.board.get_empties()

        # First move
        if len(empty_tiles) is board_len*board_len:
            # We want to fill the centre square if we're going first
            move = self.board.board_centre
        else:
            # First check for any potential win states
            move = self.check_for_win(board, board_len, empty_tiles)

            if move is None:
                # Second move
                if len(empty_tiles) is board_len*board_len-1:
                    if self.board.board_centre in empty_tiles:
                        move = self.board.board_centre
                    else:
                        move = self.board.board_corners[random.randint(0,len(self.board.board_corners)-1)]
                else:
                    # Anything else we pick a random tile
                    move = random.randint(0, self.board.board_len*self.board.board_len-1)

                    while move not in empty_tiles:
                        move = random.randint(0, self.board.board_len*self.board.board_len-1)


        # Fill the tile
        self.board.assign_move(move, self.mark)

        return move

    def check_for_win(self, board, board_len, empty_tiles):
        """ Function for checking for any win (or loss) states
        """
        defensive_moves = set()

        # Verticals
        for move in empty_tiles:
            col = []
            row = []
            # Build rows and columns
            for i in range(board_len):
                col.append(board[i][move%board_len])
                row.append(board[move/board_len][i])

            # Horizontal checks
            if row.count(None) is 1 and len(filter(None, set(row))) is 1 and self.mark in row:
                return move
            elif row.count(None) is 1 and len(filter(None, set(row))) is 1:
                defensive_moves.add(move)

            # Vertical checks
            if col.count(None) is 1 and len(filter(None, set(col))) is 1 and self.mark in col:
                return move
            elif col.count(None) is 1 and len(filter(None, set(col))) is 1:
                defensive_moves.add(move)

        diag_a = {}
        diag_b = {}
        for i in range(board_len):
            # Build diagonals
            diag_a[self.board.convert_tile(i,i)] = board[i][i]
            diag_b[self.board.convert_tile(i, (board_len-1-i))] =  board[i][board_len-1-i]

        # Diagonal checks
        # We're making the assumption that the winning number of tiles will always be the same as board_len.
        # Still kinda ugly though.
        if diag_a.values().count(None) is 1 and len(filter(None, set(diag_a.values()))) is 1 and self.mark in diag_a:
            for move, val in diag_a.items():
                if val is None:
                    defensive_moves.add(move)
        elif diag_a.values().count(None) is 1 and len(filter(None, set(diag_a.values()))) is 1:
            for move, val in diag_a.items():
                if val is None:
                    defensive_moves.add(move)

        if diag_b.values().count(None) is 1 and len(filter(None, set(diag_b.values()))) is 1 and self.mark in diag_b:
            for move, val in diag_b.items():
                if val is None:
                    defensive_moves.add(move)
        elif diag_b.values().count(None) is 1 and len(filter(None, set(diag_b.values()))) is 1:
            for move, val in diag_b.items():
                if val is None:
                    defensive_moves.add(move)

        # No winning move found, play a defensive one
        if len(defensive_moves) >= 1:
            return defensive_moves.pop()
        else:
            return None


    def get_game_status(self):
        """ Helper function to get the game state
        """
        return self.game_status

class Board:
    def __init__(self):
        """ Define the board for Tic Tac Toe
        """
        self.board_len = 3
        self.board_tiles = self.build_board()
        self.board_centre = 4
        self.board_corners = self.find_corners()
        self.board_edges = self.find_edges()

    def convert_tile(self, row, col):
        """ Convert a tile from the n*n array format
        """
        return (row*self.board_len)+col

    def find_corners(self):
        """ Get all the corners
        """
        corners = []
        for i, row in enumerate(self.board_tiles):
            for j, col in enumerate(row):
                if j % (self.board_len-1) is 0 and i % (self.board_len-1) is 0:
                    corners.append(self.convert_tile(i, j))
        return corners

    def find_edges(self):
        """ Get all the edges
        """
        edges = []
        for i in range(self.board_len*self.board_len):
            if i not in self.board_corners and i is not self.board_centre:
                edges.append(i)
        return edges

    def build_board(self):
        """ Function to build the n sized board
        """
        return [[None for n in range(self.board_len)] for n in range(self.board_len)]

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
        self.board_tiles[tile / self.board_len][tile % self.board_len] = mark

    def get_tile(self, tile):
        """ Get the given tile
        """
        return self.board_tiles[tile / self.board_len][tile % self.board_len]

    def get_empties(self):
        """ Return all the empty tiles
        """
        empties = []
        for i, row in enumerate(self.board_tiles):
            for j, tile in enumerate(row):
                if tile is None:
                    empties.append(self.convert_tile(i, j))
        return empties

    def print_board(self, gameid, mark):
        """ Helper function for printing out the current board state
        """
        # Space it out a bit
        # TODO: Put information about turns here?
        print "GameID: {0}, Mark: {1}".format(gameid, mark)

        # Print the board
        for row in self.board_tiles:
            for i, tile in enumerate(row):
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
