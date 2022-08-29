#!/usr/bin/python3
import pygame
import pygame.freetype
import random
import game_colors
from datetime import datetime
from operator import itemgetter


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
        I_piece = [(0, 1, 2, 3), (3, 7, 11, 15), (0, 4, 8, 12)]
        J_piece = [(0, 4, 5, 6), (0, 1, 4, 8), (0, 1, 2, 6), (1, 5, 8, 9)]
        L_piece = [(2, 4, 5, 6), (0, 4, 8, 9), (0, 1, 2, 4), (0, 1, 5, 9)]
        O_piece = [(0, 1, 4, 5)]
        S_piece = [(1, 2, 4, 5), (0, 4, 5, 9)]
        Z_piece = [(0, 1, 5, 6), (1, 4, 5, 8)]
        T_piece = [(1, 4, 5, 6), (0, 4, 5, 8), (0, 1, 2, 5), (1, 4, 5, 9)]
        self.grid_width = 10
        self.grid_height = 20
        self.unmapped_pieces = [I_piece, J_piece, L_piece, O_piece,
                S_piece, Z_piece, T_piece]
        self.possible_pieces = self.map_pieces()
        self.in_play = True
        self.color_list = [game_colors.CYAN, game_colors.BLUE, 
                game_colors.ORANGE, game_colors.YELLOW, game_colors.GREEN, 
                game_colors.RED, game_colors.PINK]
        self.new_tetromino()

    def map_pieces(self):
        mapped_possible_pieces = []
        for piece_id, piece_all_state in enumerate(self.unmapped_pieces):
            all_states = []
            for piece_state in piece_all_state:
                single_state = []
                for index in piece_state:
                    if piece_id in (2, 4, 3, 6):
                        y_multi = index//4
                        index += y_multi*self.grid_width - 4*y_multi + self.grid_width/2 - 1
                        single_state.append(index)
                    else:
                        y_multi = index//4
                        index += y_multi*self.grid_width - 4*y_multi + self.grid_width/2 - 2
                        single_state.append(index)

                all_states.append(tuple(single_state))
            mapped_possible_pieces.append(all_states)
        return mapped_possible_pieces

    def shift_left(self):
        if 0 not in map(lambda index: index%self.grid_width, self.current_piece):
            self.current_piece = [index - 1 for index in self.current_piece]

    def shift_right(self):
        if self.grid_width-1 not in map(lambda index: index%self.grid_width, self.current_piece):
            self.current_piece = [index + 1 for index in self.current_piece]
    
    def soft_drop(self):
        if self.grid_height-1 not in map(lambda index: index//self.grid_width, self.current_piece):
            self.current_piece = [index + self.grid_width for index in self.current_piece]



    def new_tetromino(self):
        # using random piece for now but will change to randomise a buffer
        # for lower varience later.
        self.piece_id = random.randint(0, len(self.possible_pieces) - 1)
        self.rotation_num = 0
        self.current_piece = self.possible_pieces[self.piece_id][self.rotation_num]
   
    def cw_rotation(self):
        self.rotation_num = (self.rotation_num + 1)%len(self.possible_pieces[self.piece_id])
        self.current_piece = self.possible_pieces[self.piece_id][self.rotation_num]

    def ccw_rotation(self):
        self.rotation_num = (self.rotation_num - 1)%len(self.possible_pieces[self.piece_id])
        self.current_piece = self.possible_pieces[self.piece_id][self.rotation_num]

    def get_tetromino(self):
        return {"piece_id": self.piece_id, "current_piece": self.current_piece}





class game_board:
    def set_grid_dim(self, grid_width, grid_height, scale = 40, side_bar_width = 4):
        self.__scale = scale 
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.side_bar_width = side_bar_width
        self.__board = self.grid_width*self.grid_height*[-1]
        self.screen = pygame.display.set_mode((self.__scale*(self.grid_width+self.side_bar_width), 
            self.__scale*self.grid_height))
        self.color_list = [game_colors.CYAN, game_colors.BLUE, 
                game_colors.ORANGE, game_colors.YELLOW, game_colors.GREEN, 
                game_colors.RED, game_colors.PINK]
    def clear_side_bar(self):
        rect = (self.grid_width, 0, self.grid_width + self.side_bar_width, self.grid_height)
        side_bar_rect = list(self.__scale*ordin for ordin in rect)
        side_bar_rect[0] += 1
        pygame.draw.rect(self.screen, 0x0, side_bar_rect)

    def draw_fps(self, fps):
        fps_font = pygame.freetype.SysFont("Times New Roman", 25)
        fps_font.render_to(self.screen, 
                (self.__scale*(self.grid_width + 1.5), 0, 0, 0), 
                "FPS: " + fps, (255, 255, 255))

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
            else:
                self.__set_coord_color(index, 0x0)
        self.draw_grid()

    def draw_current_piece(self, current_piece, color):
        for index in current_piece:
            if color < len(self.color_list):
                self.__set_coord_color(index, self.color_list[color])

    def fun_board_func(self):
        rand_list = list(random.randint(0, len(self.color_list)-1) for _ in range(len(self.__board)))
        self.__board = rand_list
        self.draw_board()




class game:
    def __init__(self):
        pygame.init()
        delay = 130
        repeat = 100
        pygame.key.set_repeat(delay, repeat)
        self.alive = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.grid_width = 10
        self.grid_height = 20
        self.fps_goal = 144
        # define board indices from left to right then top to bottom
        self.board = game_board()
        self.board.set_grid_dim(self.grid_width, self.grid_height)
        self.board.draw_grid()
        self.board.draw_board()
        self.game_loop()

            
    def game_loop(self):
        clock = pygame.time.Clock()
        while self.alive:
            pieces = tetrimino()
            pieces.new_tetromino()
            while pieces.in_play:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pieces.in_play = False
                        self.alive = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            pieces.in_play = False
                            self.alive = False
                        if event.key == pygame.K_UP or event.key == pygame.K_x:
                            pieces.cw_rotation()
                        if event.key == pygame.K_z:
                            pieces.ccw_rotation()
                        if event.key == pygame.K_LEFT:
                            pieces.shift_left()
                        if event.key == pygame.K_RIGHT:
                            pieces.shift_right()
                        if event.key == pygame.K_DOWN:
                            pieces.soft_drop()
                        # Debug key -> get new piece with n
                        if event.key == pygame.K_n:
                            pieces.new_tetromino()
                current_piece, color = itemgetter('current_piece', 'piece_id')(pieces.get_tetromino())
                self.board.draw_board()
                self.board.draw_current_piece(current_piece, color)
                fps = str(clock.get_fps()).split(".")[0]
                self.board.clear_side_bar()
                self.board.draw_fps(fps)
                pygame.display.flip()
                clock.tick(self.fps_goal)
                





def main():
    random.seed(datetime.now().timestamp())
    new_game = game()


if __name__ == '__main__':
    main()
