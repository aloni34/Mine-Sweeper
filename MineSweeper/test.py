import pandas as pd
from values import *
import os


class Test(object):

    def __init__(self, connector, root):

        self.connector = connector

        self.root = root

        self.number_of_tests = S_T.NUMBER_OF_TESTS-1
        self.current_test = 0

        self.number_of_cycles = S_T.TEST_CYCLE-1
        self.current_cycle = 0

        self.amount_of_bombs_on_the_board_in_the_start = S_T.AMOUNT_OF_BOMBS

        self.df1 = self.create_raw_data_dataframe()
        self.df2 = self.create_summarize_dataframe()

    # region Methods
    @ staticmethod
    def create_raw_data_dataframe():

        data = {
            'Success': [],
            'Won': [],
        }

        return pd.DataFrame(data)

    @ staticmethod
    def create_summarize_dataframe():

        data = {
            'Wins Amount': [],
            'Wins Percentage': [],
            'Losses Amount': [],
            'Losses Percentage': [],

        }

        return pd.DataFrame(data)

    def update_data(self, data):
        self.df1.loc[len(self.df1)] = [data[0], data[1]]
        self.current_test += 1

    def update_cycle(self):
        self.current_cycle += 1
        self.current_test = 0
        S_T.AMOUNT_OF_BOMBS += S_T.STEP
        self.df1 = self.create_raw_data_dataframe()
        self.df2 = self.create_summarize_dataframe()

    def print_details(self):

        print(self.df1.describe())
        print(self.df1)

        # conditions
        first_condition = self.df1['Won'] == True
        second_condition = self.df1['Success'] > 90

        # summarize win / loss details
        result_wins = len(self.df1[first_condition]['Success'])
        percent_wins = str(round((result_wins / S_T.NUMBER_OF_TESTS) * 100, 2)) + "%"
        result_losses = len(self.df1[~first_condition]['Success'])
        percent_losses = str(round((result_losses / S_T.NUMBER_OF_TESTS) * 100, 2)) + "%"

        # save in a dataframe
        self.df2.loc[len(self.df2)] = [result_wins, percent_wins, result_losses, percent_losses]

        print(f"Amount of wins: {result_wins} Percentage: {percent_wins}\n"
              f"Amount of Losses: {result_losses} Percentage: {percent_losses}")

    def save_as_a_new_file(self):

        directory = f"Data/Samples/{S_T.BOARD_HEIGHT}X{S_T.BOARD_WIDTH}"
        filename = f"{S_T.BOARD_HEIGHT}X{S_T.BOARD_WIDTH}-{S_T.AMOUNT_OF_BOMBS}.xlsx"
        path = os.path.join(directory, filename)

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Save the DataFrame to the specified path
        with pd.ExcelWriter(path, engine='openpyxl') as writer:
            self.df1.to_excel(writer, sheet_name='Sheet1', index=False)
            self.df1.describe().to_excel(writer, sheet_name='Sheet2', index=False)
            self.df2.to_excel(writer, sheet_name='Sheet3', index=False)

        print(f"File saved to: {path}")
    # endregion
