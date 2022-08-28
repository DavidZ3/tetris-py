#!/usr/bin/python3
import pygame
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
        self.color_list = [game_colors.CYAN, game_colors.BLUE, 
                game_colors.ORANGE, game_colors.YELLOW, game_colors.GREEN, 
                game_colors.RED, game_colors.PINK]

    def set_grid_dim(self, grid_width, grid_height, scale = 40, side_bar_width = 4):
        self.__scale = scale 
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.side_bar_width = side_bar_width
        self.__board = self.grid_width*self.grid_height*[-1]
        self.screen = pygame.display.set_mode((self.__scale*(self.grid_width+self.side_bar_width), 
            self.__scale*self.grid_height))

    def draw_grid(self):
        grid_color = game_colors.WHITE
        for horizontal_line in range(self.grid_height+1):
            pygame.draw.line(self.screen, grid_color, 
                    (0, self.__scale*horizontal_line), 
                    (self.__scale*self.grid_width, self.__scale*horizontal_line))

        for vertical_line in range(self.grid_width+1):
            pygame.draw.line(self.screen, grid_color, 
                    (self.__scale*vertical_line, 0), 
                    (self.__scale*vertical_line, self.__scale*self.grid_height))

    def __set_coord_color(self, index, color):
        index_x = index%self.grid_width
        index_y = index//self.grid_width

        rect = (index_x, index_y, 1, 1)
        rect_scaled = tuple( self.__scale*ordin for ordin in rect)
        pygame.draw.rect(self.screen, color, rect_scaled)

    def draw_board(self):
        for index, color_index in enumerate(self.__board):
            if color_index != -1:
                self.__set_coord_color(index, self.color_list[color_index])
        self.draw_grid()

    def fun_board_func(self):
        rand_list = list(random.randint(0, len(self.color_list)-1) for _ in range(len(self.__board)))
        self.__board = rand_list
        self.draw_board()




class game:
    def __init__(self):
        self.alive = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.grid_width = 10
        self.grid_height = 20
        self.fps_goal = 60
        # define board indices from left to right then top to bottom
        self.board= game_board()
        self.board.set_grid_dim(self.grid_width, self.grid_height)
        self.board.draw_grid()
        self.board.draw_board()
        self.game_loop()

            
    def game_loop(self):
        # clock = pygame.time.Clock()
        while self.alive:
            new_piece = tetrimino()
            while new_piece.in_play:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        new_piece.in_play = False
                        self.alive = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP or event.key == pygame.K_x:
                            new_piece.cw_rotation()
                        if event.key == pygame.K_z:
                            new_piece.ccw_rotation()
                self.board.fun_board_func()
                pygame.time.wait(1000//self.fps_goal)
                pygame.display.flip()





def main():
    random.seed(datetime.now().timestamp())
    new_game = game()


if __name__ == '__main__':
    main()
