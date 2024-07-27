from mine_sweeper import *
from view import *
from brain import *
from test import Test


class Connector(object):

    def __init__(self, row, col, root, start):

        self.start = start
        self.model = Model(row, col, self)
        self.view = View(row, col, self, root)
        self.brain = ProbBrainOptimised(row, col, self, root, self.model, self.view)
        self.test = Test(self, root)

    # region Methods

    def play(self, row, col):
        return self.model.play(row, col)

    def mark_bomb(self, row, col):
        return self.model.board[row][col] == 0 or self.model.board[row][col] > 8

    def check_if_found_all_bombs(self, marked_bombs):
        return self.model.check_if_found_all_bombs(marked_bombs)

    def clean_probabilities_from_assured_empty_places(self):
        self.view.clean_probabilities_from_assured_empty_places(self.model.clean_probabilities_from_assured_empty_places())

    def update_if_all_marked_bombs_right(self):
        self.view.update_if_all_marked_bombs_right()

    def close_call_backs(self):
        self.view.close_call_backs()

    def restart(self):
        self.start.restart()

    def brain_play(self):
        return self.brain.play()

    def reset(self):
        self.view.reset()
        self.model.reset()
        self.brain.reset()

    def update_tests(self, data):

        if self.test.current_test < self.test.number_of_tests:
            print(self.test.current_test)
            self.reset()
            self.brain_play()
            self.test.update_data(data)

        elif self.test.current_test == self.test.number_of_tests:  # in the last test get over here
            self.test.update_data(data)
            self.test.print_details()

            # save in an Excel
            if S_T.IS_TO_SAVE:
                self.test.save_as_a_new_file()

            # update the end of a cycle
            self.test.update_cycle()

            if self.test.current_cycle < S_T.TEST_CYCLE:  # if there are more cycles, this would handle this
                self.reset()
                self.brain_play()
                self.test.update_data(data)
            else:
                S_T.AMOUNT_OF_BOMBS = self.test.amount_of_bombs_on_the_board_in_the_start

    # endregion
