#!/usr/bin/python3
import pygame
import colored
import random
import game_colors
from datetime import datetime


#   All inital tetris pieces (tetromino) can fit on a 2x4 grid
#   If we include rotations then all pieces fit on 4x4 grid
#
#   O-piece
#   **--
#   **--
#   ----
#   ----
#
#   I-piece
#   ****
#   ----
#   ----
#   ----
#
#   L-piece
#   --*-
#   ***-
#   ----
#   ----
#
#   J-piece
#   *---
#   ***-
#   ----
#   ----
#
#   S-piece
#   -**-
#   **--
#   ----
#   ----
#
#   Z-piece
#   **--
#   -**-
#   ----
#   ----
#
#   T-piece
#   -*--
#   ***-
#   ----
#   ----
#
#   Since 2D arrays are a pain, we shall represent a 4x4 matrix as such:
#   0  1  2  3
#   4  5  6  7
#   8  9  10 11
#   12 13 14 15

class tetrimino:
    def __init__(self):
        I_piece = ((0, 1, 2, 3), (3, 7, 11, 15), (0, 4, 8, 12))
        J_piece = ((0, 4, 5, 6), (0, 1, 4, 8), (0, 1, 2, 6), (1, 5, 8, 9))
        L_piece = ((2, 4, 5, 6), (0, 4, 8, 9), (0, 1, 2, 4), (0, 1, 5, 9))
        O_piece = ((0, 1, 4, 5))
        S_piece = ((1, 2, 4, 5), (0, 4, 5, 9))
        Z_piece = ((0, 1, 5, 6), (1, 4, 5, 8))
        T_piece = ((1, 4, 5, 6), (0, 4, 5, 8), (0, 1, 2, 5), (1, 4, 5, 9))
        self.possible_pieces = (I_piece, J_piece, L_piece, O_piece,
                S_piece, Z_piece, T_piece)
        self.in_play = True
        self.get_tetromino()

    def get_tetromino(self):
        # using random piece for now but will change to randomise a buffer
        # for lower varience later.
        self.piece_id = 0
        self.piece_id = random.randint(0, len(self.possible_pieces) - 1)
        self.rotation_num = 0
        self.current_piece = self.possible_pieces[self.piece_id][self.rotation_num]

    def cw_rotation(self):
        self.rotation_num = (self.rotation_num + 1)%len(self.possible_pieces[self.piece_id])
        self.current_pos = self.possible_pieces[self.piece_id][self.rotation_num]
        return

    def ccw_rotation(self):
        self.rotation_num = (self.rotation_num - 1)%len(self.possible_pieces[self.piece_id])
        self.current_pos = self.possible_pieces[self.piece_id][self.rotation_num]

class game_board:
    def __init__(self):
        pygame.init()

    def set_grid_dim(self, grid_width, grid_height, scale = 50, side_bar_width = 4):
        self.__scale = scale 
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.side_bar_width = side_bar_width

    def draw_grid(self):
        grid_color = game_colors.WHITE

        self.screen = pygame.display.set_mode((self.__scale*(self.grid_width+self.side_bar_width), 
            self.__scale*self.grid_height))

        for horizontal_line in range(self.grid_height+1):
            pygame.draw.line(self.screen, grid_color, 
                    (0, self.__scale*horizontal_line), 
                    (self.__scale*self.grid_width, self.__scale*horizontal_line))

        for vertical_line in range(self.grid_width+1):
            pygame.draw.line(self.screen, grid_color, 
                    (self.__scale*vertical_line, 0), 
                    (self.__scale*vertical_line, self.__scale*self.grid_height))

    def draw_piece(piece_id):






class game:
    def __init__(self):
        self.alive = True
        self.score = 0
        self.level = 1
        self.grid_width = 10
        self.grid_height = 20
        # define board indices from left to right then top to bottom
        self.board= game_board()
        self.board.set_grid_dim(self.grid_width, self.grid_height)
        self.board.draw_grid()
        self.game_loop()

            
    def game_loop(self):
        while self.alive:
            new_piece = tetrimino()
            while new_piece.in_play:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        new_piece.in_play = False
                        self.alive = False

                pygame.display.flip()



def main():
    random.seed(datetime.now().timestamp())
    new_game = game()


if __name__ == '__main__':
    main()
