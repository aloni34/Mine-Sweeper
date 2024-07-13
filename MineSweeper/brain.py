from values import *
import random
import time

class max_brain(object):

    def __init__(self, row, col, connector, root, model, view):

        self.root = root
        self.view = view
        self.model = model
        self.connector = connector
        self.length_row = row
        self.length_col = col

        self.board = []

        self.board = self.model.board
        self.board_copy = []

        self.bomb_places = self.model.bomb_places # real bomb places
        self.bomb_guess_places = [] # guessed bomb places

        self.probabiliy_places = {} # format of {value: max_probability}
        self.traveled_places = {} # format of {value: value}

        self.is_probabilities_rechecked = False

    def play(self):

        # first move
        self.first_play()

        # as long as there are available moves
        while self.probabiliy_places != {}:

            self.root.update()
            time.sleep(S_T.DELAY_MODIFIER)

            # retrieve the maximum probability
            max_place = max(self.probabiliy_places, key=self.probabiliy_places.get)
            max_probability = self.probabiliy_places[max_place]

            # bomb over there
            if max_probability == 1:
                self.maximum_assured(max_place)

            else:

                # retrieve the minimum probability
                min_place = min(self.probabiliy_places, key=self.probabiliy_places.get)
                min_probability = self.probabiliy_places[min_place]

                # click assured (no bomb)
                if min_probability == 0:
                    self.minimum_assured(min_place)

                # possibility that missed places that are not updated for the correct probability
                elif not self.is_probabilities_rechecked:
                    self.is_probabilities_rechecked = True
                    self.recheck_probabilities()

                # in the case we rechecked the probabilities and still didn't obtain assured 100% or 0% probability
                # then we choose the lowest place and hope it isn't a bomb
                else:
                    time.sleep(3)
                    self.is_probabilities_rechecked = False
                    self.minimum_assured(min_place)
                    # if we lost
                    if self.model.is_lost:
                        break

        # clean the unnecessary text from the board
        self.connector.clean_probabilities_from_assured_empty_places()

        # reveal bomb places and show if we won
        self.connector.update_if_all_marked_bombs_right()
        self.root.update()

        # how much the algorithm succeeded
        print(self.check_bombs_accuracy())

    # check the probability
    def probability_checker(self, moves):

        updates = []

        for move in moves:
            row = move[0]
            col = move[1]

            all_near = self.model.get_next_moves_expanded(row, col) # all places near by
            p_checks = [near for near in all_near if self.board_copy[near[0]][near[1]] in [0, 9]]  # undiscovered places
            p_placed = [near for near in all_near if self.board_copy[near[0]][near[1]] in [-2]]  # discovered places

            amount_of_checks = len(p_checks)
            amount_of_checked = len(p_placed)

            # no more checks (no bombs)
            if amount_of_checked == self.board[row][col]:
                for p_check in p_checks:

                    place = p_check[0] * self.length_col + p_check[1]  # position

                    self.probabiliy_places[place] = 0
                    updates.append([p_check[0], p_check[1], 0])

            # all the other places nearby are bombs (all bombs)
            elif amount_of_checks == self.board[row][col] - amount_of_checked:
                for p_check in p_checks:

                    place = p_check[0] * self.length_col + p_check[1]  # position

                    self.probabiliy_places[place] = 1
                    updates.append([p_check[0], p_check[1], 1])

            # check if there are available places
            elif amount_of_checks > 0:
                if amount_of_checked == 0:
                    probability = round(1 / (amount_of_checks - amount_of_checked), 2)
                else:
                    probability = round(1 / amount_of_checks, 2)

                for p_check in p_checks:

                    place = p_check[0] * self.length_col + p_check[1] # position

                    if place not in self.probabiliy_places:
                        self.probabiliy_places[place] = probability
                        updates.append([p_check[0], p_check[1], probability])

                    elif 0 < self.probabiliy_places[place] < probability:
                        self.probabiliy_places[place] = probability
                        updates.append([p_check[0], p_check[1], probability])

        return updates

    # first turn
    def first_play(self):

        # random row
        row = random.randint(0, self.length_row-1) # random row
        # random col
        col = random.randint(0, self.length_col-1) # random col

        # play first turn in the model
        updates = self.connector.play(row, col)

        # update the view details
        self.view.update_labels(updates)

        # copy a replica of the current board for adjustment and checks for bomb locations
        # and for changes which were made in the other board.
        # note that we only use the bomb location for calculation of the number of labels, not for assured placement,
        # this is made by our probability.
        self.board_copy = self.copy_board()

        # update the replica board
        self.update_board(updates)

        # places where there are bombs near of them
        p_places = self.probability_checker([move for move in updates if 1 <= self.board_copy[move[0]][move[1]] <= 8])

        # visualize the probabilities on the board
        self.view.show_text(p_places)

    # probability of 100 % (1) - bomb
    def maximum_assured(self, max_place):

        if max_place in self.traveled_places:
            del self.probabiliy_places[max_place]
        else:
            self.traveled_places[max_place] = max_place

            row = max_place // self.length_col
            col = max_place % self.length_col

            self.board_copy[row][col] = -2  # the number which presents marked bombs

            # add the guessed bomb location for the list
            self.bomb_guess_places.append([row, col])

            if [row, col] not in self.view.marked_bombs:
                self.view.mark_bomb(row, col)

            del self.probabiliy_places[max_place]

            # update the probabilities of the surrounding labels where there are bombs near of them
            near_positions = self.model.get_next_moves_expanded(row, col)
            near_positions = [move for move in near_positions if 1 <= self.board[move[0]][move[1]] <= 8]
            p_places = self.probability_checker(near_positions)

            self.view.show_text(p_places)

    # probability of 0 % (0) - no bomb
    def minimum_assured(self, min_place):

        if min_place in self.traveled_places:
            del self.probabiliy_places[min_place]
        else:
            self.traveled_places[min_place] = min_place

            row = min_place // self.length_col
            col = min_place % self.length_col

            # update the model that we click and receive updates about new places that we can check
            updates = self.connector.play(row, col)
            self.view.update_labels(updates)  # update the view details
            self.update_board(updates)  # update the replica board
            p_places = self.probability_checker(updates)  # places where there are bombs near of them

            self.view.show_text(p_places)
            del self.probabiliy_places[min_place]

            # get the additional places near by and their probabilities
            near_positions = self.model.get_next_moves_expanded(row, col)
            near_positions = [move for move in near_positions if 1 <= self.board[move[0]][move[1]] <= 8]

            p_places = self.probability_checker(near_positions)
            self.view.show_text(p_places)

            # removes updates from the required checking if they returned as values
            self.remove_updates_from_probabilities(updates)

    # recheck probabilities - sometimes the algorithm can't update all the probabilities, so we have to recheck updates
    def recheck_probabilities(self):

        updates = []
        self.remove_checked_probabilities()

        # for every probability_place left -> convert it for a list
        for key in self.probabiliy_places:
            value = self.probabiliy_places[key]

            row = key // self.length_col
            col = key % self.length_col

            updates.append([row, col])

        moves = {}
        for update in updates:
            near_positions = self.model.get_next_moves_expanded(update[0], update[1])
            near_positions = [move for move in near_positions if 1 <= self.board[move[0]][move[1]] <= 8]

            for place in near_positions:
                value = place[0] * self.length_col + place[1]
                if value not in moves:
                    moves[value] = [place[0], place[1]]

        for move in moves:
            p_places = self.probability_checker([moves[move]])
            for p_place in p_places:
                if p_place in self.view.marked_bombs:
                    p_places.remove(p_place)

    def copy_board(self):

        lst = []

        for i in range(self.length_row):

            inner_lst = []

            for j in range(self.length_col):

                inner_lst.append(self.model.board[i][j])

            lst.append(inner_lst)

        return lst

    def check_bombs_accuracy(self):

        success_guess = 0
        failed_guess = 0

        for bomb_place in self.bomb_places:
            if bomb_place in self.bomb_guess_places:
                success_guess += 1
            else:
                failed_guess += 1

        return "Accuracy: " + str(round((success_guess / len(self.bomb_places)) * 100, 2)) + "%\nSuccess guesses: " + str(success_guess) + "\nFailed guesses: " + str(failed_guess)

    def update_board(self, updates):
        for update in updates:
            self.board_copy[update[0]][update[1]] = update[2]

    # remove duplicates
    def remove_updates_from_probabilities(self, updates):
        for update in updates:
            place = update[0] * self.length_col + update[1]  # position
            if place in self.probabiliy_places:
                del self.probabiliy_places[place]

    # remove checked places - possible to obtain checked probabilities, so we have to remove them
    def remove_checked_probabilities(self):
        keys_to_remove = self.traveled_places.keys()

        for key in keys_to_remove:
            if key in self.probabiliy_places:
                del self.probabiliy_places[key]
