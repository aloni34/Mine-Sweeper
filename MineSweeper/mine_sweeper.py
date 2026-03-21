import random
from values import *
import pandas as pd


class Model(object):

    def __init__(self, rows, columns, connector):

        self.available_place = []
        self.amount_of_mines = S_T.AMOUNT_OF_BOMBS
        self.length_row = rows
        self.length_col = columns

        self.update_places = []  # format of [row, col, value]
        self.bomb_places = []  # format of [row, col]

        self.is_first = True
        self.is_lost = False

        # connections
        self.connector = connector

        # if we play on downloaded maps
        if S_T.IS_TO_LOAD:
            self.maps = self.download()
            self.cur_map = 0  # index of the map
            self.from_string_to_2d_board()
            S_T.NUMBER_OF_TESTS = len(self.maps)
        else:
            self.board = self.create_board(self.length_row, self.length_col)

    # region Methods
    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def play(self, row, col):
        self.update_places = []

        if self.is_first:
            self.handle_first_move(row, col)
        else:
            self.handle_subsequent_move(row, col)

        return self.update_places

    def handle_first_move(self, row, col):
        self.is_first = False
        self.first_place_on_board(row, col)

        # Initialize available places and remove the first move
        self.available_place = self.available_places()
        self.available_place.remove([row, col])

        # Remove additional places around the first move from available places
        for place in self.filter_moves(self.get_next_moves_expanded(row, col), 0):
            self.available_place.remove(place)

        # Place mines and perform the first recursive placement
        self.place_mines()
        self.recursive_placement(row, col)

    def handle_subsequent_move(self, row, col):
        if self.board[row][col] == 0:
            self.recursive_placement(row, col)
        elif self.board[row][col] == 9:
            print("You lost!\nLanded on a bomb")
            if S_T.IS_TO_VIEW:
                self.connector.case_reveal()
            self.is_lost = True
        else:
            print("Invalid Place")

    def recursive_placement(self, row, col):

        # Count the number of bombs nearby
        nearby_bombs = len(self.filter_moves(self.get_next_moves_expanded(row, col), 9))

        # If no bombs are nearby, continue the recursion
        if nearby_bombs == 0:
            self.board[row][col] = -1  # Mark the current place as checked
            self.update_places.append([row, col, -1])

            # Get the next available moves
            moves = self.filter_moves(self.get_next_moves_expanded(row, col), 0)

            # If there are no moves, end the operation
            if not moves:
                return

            # Recursively check the next empty spaces
            for move in moves:
                self.recursive_placement(move[0], move[1])
        else:
            # If bombs are nearby, update the current place with the bomb count
            self.board[row][col] = nearby_bombs
            self.update_places.append([row, col, nearby_bombs])

    def first_place_on_board(self, row, col):
        self.board[row][col] = -1

    def create_board(self, rows, columns):
        return [[0 for i in range(columns)] for j in range(rows)]

    def available_places(self):
        return [[row, col] for row in range(len(self.board)) for col in range(len(self.board[0]))]

    def place_mines(self):
        if S_T.IS_TO_LOAD:
            for i in self.bomb_places:
                self.available_place.remove(i)
        else:
            for _ in range(self.amount_of_mines):
                position = random.choice(self.available_place)
                self.board[position[0]][position[1]] = 9
                self.available_place.remove(position)
                self.bomb_places.append(position)

    def get_next_moves(self, row, col):  # 4 places

        directions = [
            (1, 0),  # Down
            (-1, 0),  # Up
            (0, 1),  # Right
            (0, -1)  # Left
        ]

        next_moves = [
            [row + dr, col + dc]
            for dr, dc in directions
            if 0 <= row + dr < self.length_row and 0 <= col + dc < self.length_col
        ]

        return next_moves

    def get_next_moves_expanded(self, row, col):  # 8 places

        directions = [
            (1, 0),  # Down
            (1, 1),  # Down-Right
            (1, -1),  # Down-Left
            (-1, 0),  # Up
            (-1, 1),  # Up-Right
            (-1, -1),  # Up-Left
            (0, 1),  # Right
            (0, -1)  # Left
        ]

        next_moves = [
            [row + dr, col + dc]
            for dr, dc in directions
            if 0 <= row + dr < self.length_row and 0 <= col + dc < self.length_col
        ]

        return next_moves

    def filter_moves(self, moves, value_to_keep):
        return [move for move in moves if self.board[move[0]][move[1]] == value_to_keep]

    def check_if_found_all_bombs(self, marked_bombs):
        return all(marked_bomb in self.bomb_places for marked_bomb in marked_bombs)

    def clean_probabilities_from_assured_empty_places(self):

        empty_places = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] <= 0 or self.board[row][col] == 9:
                    empty_places.append([row, col])
        return empty_places

    def download(self):
        df = pd.read_excel(f'Data/Boards/{S_T.BOARD_HEIGHT}X{S_T.BOARD_WIDTH}/{S_T.BOARD_HEIGHT}X'
                           f'{S_T.BOARD_WIDTH}-{S_T.AMOUNT_OF_BOMBS}.xlsx')
        return df

    def from_string_to_2d_board(self):
        # Adjust the column name and row index as needed

        board_string = self.maps['Maps'][self.cur_map]

        board_2d = []
        position = 0

        for i in range(S_T.BOARD_HEIGHT):
            row = []
            for j in range(S_T.BOARD_WIDTH):
                value = int(board_string[position])
                row.append(value)
                position += 1
                if value == 9:
                    self.bomb_places.append([i, j])

            board_2d.append(row)

        self.board = board_2d
        self.cur_map += 1

    def reset(self):

        self.board = self.create_board(self.length_row, self.length_col)
        self.available_place = []
        self.amount_of_mines = S_T.AMOUNT_OF_BOMBS

        self.update_places = []  # format of [row, col, value]
        self.bomb_places = []  # format of [row, col]

        self.is_first = True
        self.is_lost = False

        if S_T.IS_TO_LOAD:
            self.from_string_to_2d_board()
        else:
            self.board = self.create_board(self.length_row, self.length_col)

    # endregion
