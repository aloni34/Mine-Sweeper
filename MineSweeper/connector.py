from mine_sweeper import *
from view import *
from brain import *

class Connector(object):

    def __init__(self, row , col, root, start):

        self.start = start
        self.model = model(row, col, self)
        self.view = view(row, col, self, root)
        self.brain = max_brain(row, col, self, root, self.model, self.view)

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
        self.brain.play()

    # endregion