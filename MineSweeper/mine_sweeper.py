import random
from values import *

class model(object):

    def __init__(self, rows, columns, connector):

        self.board = self.create_board(rows, columns)
        self.available_place = []
        self.amount_of_mines = S_T.AMOUNT_OF_BOMBS
        self.length_row = rows
        self.length_col = columns

        self.update_places = []
        self.bomb_places = []

        self.is_first = True

        # connections
        self.connector = connector

    # region Methods

    def print_board(self):
        for i in self.board:
            print(i)

    def play(self, row, col):

        self.update_places = []

        if self.is_first: # first move

            self.is_first = False
            self.first_place_on_board(row, col)

            # input how many mines
            #self.amount_of_mines = int(input("enter how many mines "))

            # check for available places
            self.available_place = self.available_places()
            self.available_place.remove([row,col])


            # add additional places around the first place and remove them from available places for bombs
            additional_places = self.get_next_moves_expanded(row, col, 0)
            for place in additional_places:
                self.available_place.remove(place)

            # places mines
            self.place_mines()
            self.recursive_placement(row, col)


        else: # after the first move

            # landed on an empty place
            if self.board[row][col] == 0:
                self.recursive_placement(row, col)

            else:
                # In the case where landed on a bomb
                if self.board[row][col] == 9:
                    print("You lost!\nLanded on a bomb")
                    self.connector.view.case_reveal()
                # Marked other invalid place; somewhere which was already checked
                else:
                    print("Invalid Place")

        return self.update_places

    def recursive_placement(self, row, col):

        # check for bombs near by, if there are, then, don't continue the recursive operation, else, continue
        amount_of_bombs_near = len(self.get_next_moves_expanded(row, col, 9))

        # if there are no bombs near by
        if amount_of_bombs_near == 0:

            # place the current place as a check place
            self.board[row][col] = -1
            # adds the place to update for checked value
            self.update_places.append([row, col, -1])

            # obtain the next available moves
            moves = self.get_next_moves_expanded(row, col, 0)

            # no moves, end operation
            if moves == []:
                return

            # continue to check for the next empty spaces
            for move in moves:
                # this check is here for the case an available place that was available before is no longer available (update was made in the recursive check)
                if self.board[move[0]][move[1]] == 0:
                    # continue to check for more available moves
                    self.recursive_placement(move[0], move[1])


        else:
            # in the case there are bombs near by, update the current place to be the number of bombs near by
            self.board[row][col] = amount_of_bombs_near
            self.update_places.append([row, col, amount_of_bombs_near])

        return

    def first_place_on_board(self, row, col):
        self.board[row][col] = -1

    def create_board(self, rows, columns):
        return [[0 for i in range(columns)] for j in range(rows)]

    def available_places(self):

        lst = []
        row_len = len(self.board)
        col_len = len(self.board[0])

        for row in range(row_len):
            for col in range(col_len):
                lst.append([row,col])

        return lst

    def place_mines(self):

        for i in range(self.amount_of_mines):

            position = random.choice(self.available_place)
            self.board[position[0]][position[1]] = 9
            self.available_place.remove(position)
            self.bomb_places.append(position)

        self.available_place = []

    def get_next_moves(self, row, col, required_value): # 4 places

        next_moves = []

        if row+1 < self.length_row:
            next_moves.append([row + 1, col]) # ->

        if row-1 >= 0:
            next_moves.append([row - 1, col])  # <-

        if col+1 < self.length_col:
            next_moves.append([row, col + 1])  # V

        if col-1 >= 0:
            next_moves.append([row, col - 1])  # ^

        # removes moves where the value is not the value given
        for move in next_moves:
            if self.board[move[0]][move[1]] != required_value:
                next_moves.remove(move)

        return next_moves

    def get_next_moves_expanded(self, row, col, required_value): # 8 places

        next_moves = []

        if row+1 < self.length_row:
            next_moves.append([row + 1, col]) # ->
            if col + 1 < self.length_col:
                next_moves.append([row + 1, col + 1])  # V->
            if col - 1 >= 0:
                next_moves.append([row + 1, col - 1])  # ^->

        if row-1 >= 0:
            next_moves.append([row - 1, col])  # <-
            if col + 1 < self.length_col:
                next_moves.append([row - 1, col + 1])  # <-V
            if col - 1 >= 0:
                next_moves.append([row - 1, col - 1])  # <-^

        if col+1 < self.length_col:
            next_moves.append([row, col + 1])  # V

        if col-1 >= 0:
            next_moves.append([row, col - 1])  # ^

        # Filter moves where the value is not the required value
        next_moves = [move for move in next_moves if self.board[move[0]][move[1]] == required_value]

        return next_moves

    def check_if_found_all_bombs(self, marked_bombs):
        for marked_bomb in marked_bombs:
            if marked_bomb not in self.bomb_places:
                return False
        return True

    # endregion