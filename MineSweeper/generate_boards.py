import openpyxl
from openpyxl import load_workbook
import numpy as np
import os
import pandas as pd


class BoardGenerator(object):

    # region Methods
    @staticmethod
    def generate_boards(amount, h, w, bombs, path, empty_center=False):

        data = {
            'Board': []
        }

        df1 = pd.DataFrame(data)

        if not empty_center:  # if no need to clear center, the center can have bombs
            for i in range(amount):
                board = BoardGenerator.generate_board_pure_random(h, w, bombs)
                df1.loc[len(df1)] = [board]
        else:
            for i in range(amount):  # if it is required to have clear center
                board = BoardGenerator.generate_board_empty_center(h, w, bombs)
                df1.loc[len(df1)] = [board]

        BoardGenerator.save_board_to_excel_better(df1, f'{path}/{h}X{w}', f'{h}X{w}-{bombs}.xlsx')

    @staticmethod
    def generate_board_pure_random(h, w, bombs):

        # Initialize an empty board
        board = np.zeros((h, w), dtype=int)

        # Flatten the board to a 1D array to make it easier to pick random positions
        flat_board = board.flatten()

        # Randomly select k unique positions to place bombs
        bomb_positions = np.random.choice(h * w, bombs, replace=False)

        # Place bombs (represented by 9) at the selected positions
        flat_board[bomb_positions] = 9

        return flat_board

    @staticmethod
    def generate_board_empty_center(h, w, bombs):
        # Initialize an empty board
        board = np.zeros((h, w), dtype=int)

        # Define the center and its surrounding cells
        center_x, center_y = h // 2, w // 2
        protected_area = [
            (center_x - 1, center_y - 1), (center_x - 1, center_y), (center_x - 1, center_y + 1),
            (center_x, center_y - 1), (center_x, center_y), (center_x, center_y + 1),
            (center_x + 1, center_y - 1), (center_x + 1, center_y), (center_x + 1, center_y + 1)
        ]

        # Flatten the board to a 1D array to make it easier to pick random positions
        flat_board = board.flatten()

        # Generate a list of all possible positions except the protected area
        all_positions = [(i // w, i % w) for i in range(h * w)]
        available_positions = [pos for pos in all_positions if pos not in protected_area]

        # Convert available positions back to 1D indices
        available_indices = [pos[0] * w + pos[1] for pos in available_positions]

        # Randomly select k unique positions to place bombs
        bomb_positions = np.random.choice(available_indices, bombs, replace=False)

        # Place bombs (represented by 9) at the selected positions
        flat_board[bomb_positions] = 9

        return flat_board

    @staticmethod
    def save_board_to_excel_better(boards, directory, filename):

        path = os.path.join(directory, filename)

        try:  # Load the workbook and select the active worksheet
            workbook = load_workbook(path)
            sheet = workbook.active
        except FileNotFoundError:  # If the file doesn't exist, create a new workbook and select the active worksheet
            workbook = openpyxl.Workbook()
            sheet = workbook.active

        sheet.cell(row=1, column=1, value="Maps")

        for index in range(len(boards)):  # Saves in a single excel
            board = boards["Board"][index]
            board = ''.join(map(str, board))
            sheet.cell(row=index+2, column=1, value=board)

        #  Saves the workbook
        workbook.save(path)

    # endregion


# This might take a while, depends on the amount of boards required and the amount per excel
BoardGenerator.generate_boards(10000, 15, 15, 25, 'Data/Boards', True)
