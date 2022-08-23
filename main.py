#!/usr/bin/python3
import pygame
import numpy as np


#   All inital tetris pieces (tetromino) can fit on a 2x4 grid
#
#   O-piece 
#   -**-
#   -**-
#
#   I-piece
#   ****
#   ----
#
#   L-piece
#   ---*
#   ****
#
#   J-piece
#   *---
#   ****
#
#   S-piece
#   --**
#   -**-
# 
#   Z-piece
#   **--
#   -**-
# 
#   T-piece
#   -*--
#   ***-
# 
empty_grid = np.zeros((2,6))


pieces = dict()



class game():
    def __init__(self):
        self.score = 0
        self.level = 1
        self.grid_width = 10
        self.grid_height = 20

    def generate_piece(self):

    



    


def main():
    new_game = game()


if __name__ == '__main__':
    main()
