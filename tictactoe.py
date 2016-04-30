# Tic Tac Toe module for Mergambot
# Author: Nathaniel Oon
# Date:   30/04/2016

class Board:
    def __init__(self):
        self.board_len = 9
        self.board_tiles = [None, None, None,
                            None, None, None,
                            None, None, None]

    def print_board(self):
        ''' 
            Function for printing out the current board state
        '''
        # Space it out a bit
        # TODO: Put information about turns here?
        print ""

        # Print the board
        for i, tile in enumerate(self.board_tiles):
            # Use a blank space for empty tiles
            if tile == None:
                    tile = "0"

            # Print the board
            if i == 8:
                print str(tile)
            elif (i+1) % 3 == 0:
                print str(tile)
                print "---------"
            else:
                print str(tile)+' |',


class Game:
    def __init__(self):
        ttt_board = Board()
        ttt_board.print_board()