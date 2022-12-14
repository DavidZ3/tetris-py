#!/usr/bin/python3
import pygame
import pygame.freetype
import random
import game_colors
import json
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
        # I_piece = [(0, 1, 2, 3), (3, 7, 11, 15), (0, 4, 8, 12)]
        I_piece = [(0, 1, 2, 3), (2, 6, 10, 14)]
        J_piece = [(0, 4, 5, 6), (0, 1, 4, 8), (0, 1, 2, 6), (1, 5, 8, 9)]
        L_piece = [(2, 4, 5, 6), (0, 4, 8, 9), (0, 1, 2, 4), (0, 1, 5, 9)]
        O_piece = [(0, 1, 4, 5)]
        S_piece = [(1, 2, 4, 5), (0, 4, 5, 9)]
        Z_piece = [(0, 1, 5, 6), (1, 4, 5, 8)]
        T_piece = [(1, 4, 5, 6), (0, 4, 5, 8), (0, 1, 2, 5), (1, 4, 5, 9)]
        NUM_OF_PIECE_TYPES = 7
        self.possible_piece_ids = [*range(NUM_OF_PIECE_TYPES)]
        self.new_piece_buffer_size = 2
        self.grid_width = 10
        self.grid_height = 20
        self.unmapped_pieces = [I_piece, J_piece, L_piece, O_piece,
                S_piece, Z_piece, T_piece]
        self.possible_pieces = self.map_pieces()
        self.in_play = True
        self.color_list = [game_colors.CYAN, game_colors.BLUE,
                game_colors.ORANGE, game_colors.YELLOW, game_colors.GREEN,
                game_colors.RED, game_colors.PINK]
        self.upcoming_pieces = []
        self.new_tetromino()

    def read_board(self, board):
        self.board = board

    def map_pieces(self):
        mapped_possible_pieces = []
        for piece_id, piece_all_state in enumerate(self.unmapped_pieces):
            all_states = []
            for piece_state in piece_all_state:
                single_state = []
                for index in piece_state:
                    if piece_id in (2, 4, 3, 6):
                        y_multi = index//4
                        index += y_multi*self.grid_width - 4*y_multi + self.grid_width//2 - 1
                        single_state.append(index)
                    else:
                        y_multi = index//4
                        index += y_multi*self.grid_width - 4*y_multi + self.grid_width//2 - 2
                        single_state.append(index)

                all_states.append(tuple(single_state))
            mapped_possible_pieces.append(all_states)
        return mapped_possible_pieces

    def new_tetromino(self):
        # using random piece for now but will change to randomise a buffer
        # for lower varience later.
        if self.upcoming_pieces == []:
            self.populate_upcoming_pieces()
        self.piece_id = self.upcoming_pieces.pop()
        self.rotation_num = 0
        self.current_piece = self.possible_pieces[self.piece_id]
        self.current_state = self.possible_pieces[self.piece_id][self.rotation_num]
        self.in_play = True

    def populate_upcoming_pieces(self):
        upcoming_pieces = self.new_piece_buffer_size*self.possible_piece_ids
        random.shuffle(upcoming_pieces)
        self.upcoming_pieces = upcoming_pieces



    def get_tetromino(self):
        return {"piece_id": self.piece_id, "current_state": self.current_state}


    def shift_left(self):
        new_current_piece = []
        #print(self.current_piece)
        board_idx = self.board.get_board_indices()

        # check if current_state is stuck first
        new_state = [index - 1 for index in self.current_state]
        if all(state_idx not in board_idx for state_idx in new_state):
            for state in self.current_piece:
                new_state = [index - 1 for index in state]
                if 0 not in map(lambda index: index%self.grid_width, state) and \
                    all(state_idx not in board_idx for state_idx in new_state):
                        new_current_piece.append(new_state)
                else:
                    new_current_piece.append(state)
            self.current_piece = new_current_piece
            self.current_state = new_current_piece[self.rotation_num]

    def shift_right(self):
        new_current_piece = []
        #print(self.current_piece)
        board_idx = self.board.get_board_indices()

        # check if current_state is stuck first
        new_state = [index + 1 for index in self.current_state]
        if all(state_idx not in board_idx for state_idx in new_state):
            for state in self.current_piece:
                new_state = [index + 1 for index in state]
                if self.grid_width-1 not in map(lambda index: index%self.grid_width, state) and \
                    all(state_idx not in board_idx for state_idx in new_state):
                        new_current_piece.append(new_state)
                else:
                    new_current_piece.append(state)
            self.current_piece = new_current_piece
            self.current_state = new_current_piece[self.rotation_num]

    def soft_drop(self):
        new_current_piece = []
        #print(self.current_piece)
        ghost_piece = self.board.get_ghost_piece()
        for state in self.current_piece:
            if sum(state) < sum(ghost_piece):
            #if self.grid_height-1 not in map(lambda index: index//self.grid_width, state):
                state = [index + self.grid_width for index in state]
            new_current_piece.append(state)
        self.current_piece = new_current_piece
        self.current_state = new_current_piece[self.rotation_num]


    def cw_rotation(self):
        board_idx = self.board.get_board_indices()
        inital_rotation_num = self.rotation_num
        self.rotation_num = (self.rotation_num + 1)%len(self.current_piece)
        while self.rotation_num != inital_rotation_num:
            if all(idx not in board_idx for idx in self.current_piece[self.rotation_num]):
                self.current_state = self.current_piece[self.rotation_num]
                return
            self.rotation_num = (self.rotation_num + 1)%len(self.current_piece)



    def ccw_rotation(self):
        board_idx = self.board.get_board_indices()
        inital_rotation_num = self.rotation_num
        self.rotation_num = (self.rotation_num - 1)%len(self.current_piece)
        while self.rotation_num != inital_rotation_num:
            if all(idx not in board_idx for idx in self.current_piece[self.rotation_num]):
                self.current_state = self.current_piece[self.rotation_num]
                return
            self.rotation_num = (self.rotation_num - 1)%len(self.current_piece)



class game_board:
    def read_tetromino(self, pieces):
        self.pieces = pieces

    def save_board(self):
        try:
            with open("save.json", "w+") as file:
                board_obj = {"board": self._board}
                json.dump(board_obj, file)
        except:
            print("failed to open save.json")

    def load_save(self):
        try:
            with open("save.json", "r") as file:
                self._board = json.load(file)["board"]
        except:
            print("failed to open save.json")


    def get_board_indices(self):
        board_arr = []
        for idx, piece_id in enumerate(self._board):
            if piece_id != -1:
                board_arr.append(idx)
        return board_arr

    def set_grid_dim(self, grid_width, grid_height, scale = 40, side_bar_width = 4):
        self.__scale = scale
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.side_bar_width = side_bar_width
        self._board = self.grid_width*self.grid_height*[-1]
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

    def draw_score(self, lines, score):
        score_font = pygame.freetype.SysFont("Times New Roman", 25)
        score_font.render_to(self.screen,
                (self.__scale*(self.grid_width + 0.5), 20, 0, 0),
                f"Lines: {lines}", (255, 255, 255))
        score_font.render_to(self.screen,
                (self.__scale*(self.grid_width + 0.5), 40, 0, 0),
                f"Score: {score}", (255, 255, 255))

    def draw_fps(self, fps):
        fps_font = pygame.freetype.SysFont("Times New Roman", 25)
        fps_font.render_to(self.screen,
                (self.__scale*(self.grid_width + 0.5), 0, 0, 0),
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

    def reset_board(self):
        self._board = self.grid_width*self.grid_height*[-1]
        self.draw_board()

    def get_ghost_piece(self):
        # terrible implentation for time-complexity (possible hashmap solution)
        piece_collision = False
        end_of_board  = False
        ghost_piece = self.pieces.current_state
        while not piece_collision and not end_of_board:
            new_ghost_piece = tuple(index + self.grid_width for index in ghost_piece)
            #print({"new_ghost_piece": new_ghost_piece})
            for index in new_ghost_piece:
                if index >= len(self._board):
                    end_of_board = True
                    break
                if self._board[index] != -1:
                    piece_collision = True
                    break
            if not piece_collision and not end_of_board:
                ghost_piece = new_ghost_piece
        return ghost_piece

    def draw_ghost_piece(self):
        ghost_piece = self.get_ghost_piece()
        if ghost_piece != self.pieces.current_state:
            for index in ghost_piece:
                self.__set_coord_color(index, game_colors.WHITE)

    def __set_coord_color(self, index, color):
        index_x = index%self.grid_width
        index_y = index//self.grid_width

        rect = (index_x, index_y, 1, 1)
        rect_scaled = tuple( self.__scale*ordin for ordin in rect)
        pygame.draw.rect(self.screen, color, rect_scaled)

    def draw_board(self):
        for index, color_index in enumerate(self._board):
            if color_index != -1:
                self.__set_coord_color(index, self.color_list[color_index])
            else:
                self.__set_coord_color(index, 0x0)
        self.draw_grid()

    def draw_current_state(self, current_state, color):
        for index in current_state:
            if color < len(self.color_list):
                self.__set_coord_color(index, self.color_list[color])

    def draw_all(self):
        self.draw_grid()
        self.draw_board()

    def fun_board_func(self):
        rand_list = list(random.randint(0, len(self.color_list)-1) for _ in range(len(self._board)))
        self._board = rand_list
        self.draw_board()

    def add_tetromino_to_board(self):
        drop_index = self.get_ghost_piece()
        for piece_idx in drop_index:
            self._board[piece_idx] = self.pieces.piece_id
        self.pieces.in_play = False

    def clear_full_rows(self):
        full_rows = []
        clear_rows = 0
        for row_number in range(self.grid_height):
            row = self._board[row_number*self.grid_width:(1+ row_number)*self.grid_width]
            if all(piece_id != -1 for piece_id in row):
                clear_rows += 1
            else:
                full_rows += row

        if clear_rows:
            indices_to_pad = len(self._board) - len(full_rows)
            full_rows = indices_to_pad*[-1] + full_rows
            self._board = full_rows

        return clear_rows



class game:
    def __init__(self):
        pygame.init()
        delay = 100
        repeat = 30
        pygame.key.set_repeat(delay, repeat)
        self.pieces = tetrimino()
        self.alive = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.grid_width = 10
        self.grid_height = 20
        self.fps_goal = 200
        # define board indices from left to right then top to bottom
        self.board = game_board()
        self.board.set_grid_dim(self.grid_width, self.grid_height)
        self.board.read_tetromino(self.pieces)
        self.board.draw_all()
        self.pieces.read_board(self.board)
        self.input_delay = self.fps_goal//8
        self.game_loop()


    def game_loop(self):
        clock = pygame.time.Clock()
        while self.alive:
            self.pieces.new_tetromino()
            input_cooldown = self.input_delay
            while self.pieces.in_play:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.pieces.in_play = False
                        self.alive = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.pieces.in_play = False
                            self.alive = False
                        if event.key == pygame.K_LEFT:
                            self.pieces.shift_left()
                        if event.key == pygame.K_RIGHT:
                            self.pieces.shift_right()
                        if event.key == pygame.K_DOWN:
                            self.pieces.soft_drop()
                        if input_cooldown <= 0:
                            input_cooldown = self.input_delay
                            if event.key == pygame.K_SPACE:
                                    self.board.add_tetromino_to_board()
                            if event.key == pygame.K_UP or event.key == pygame.K_x:
                                self.pieces.cw_rotation()
                            if event.key == pygame.K_z:
                                self.pieces.ccw_rotation()
                            # Debug key -> get new piece with n
                            if event.key == pygame.K_r:
                                self.board.reset_board()
                            if event.key == pygame.K_n:
                                self.pieces.new_tetromino()
                            if event.key == pygame.K_s:
                                self.board.save_board()
                            if event.key == pygame.K_l:
                                self.board.load_save()
                input_cooldown -= 1
                current_state, color = itemgetter('current_state', 'piece_id')(self.pieces.get_tetromino())
                self.board.draw_board()
                self.board.draw_ghost_piece()
                self.board.draw_current_state(current_state, color)
                clear_lines = self.board.clear_full_rows()
                self.add_score(clear_lines)
                fps = str(clock.get_fps()).split(".")[0]
                self.board.clear_side_bar()
                self.board.draw_fps(fps)
                self.board.draw_score(self.lines_cleared, self.score)
                pygame.display.flip()
                clock.tick(self.fps_goal)

    def add_score(self, clear_lines):
        if not clear_lines:
            return
        self.lines_cleared += clear_lines
        if clear_lines == 1:
            self.score += 1000
        elif clear_lines == 2:
            # 5% bonus
            self.score += 2100
        elif clear_lines == 3:
            # 10% bonus
            self.score += 3300
        else:
            # 15% bonus
            self.score += 4600

            







def main():
    random.seed(datetime.now().timestamp())
    game()


if __name__ == '__main__':
    main()
