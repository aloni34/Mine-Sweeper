from values import *
from tkinter import *
import tkinter as tk
from tkinter import ttk

class view(object):

    def __init__(self, rows, columns, connector, root):

        # connections
        self.root = root
        self.connector = connector

        # graphics
        self.frame = self.construct_frame(self.root, 0.1, 0.1, 0.8, 0.8)
        self.board = self.create_board(self.frame, rows, columns)
        self.end_button = self.construct_end_button(self.root, 0.02, 0.02, 0.05, 0.05)
        self.restart_button = self.construct_restart_button(self.root, 0.02, 0.1, 0.05, 0.05)
        self.play_ai =  self.construct_ai_button(self.root, 0.02, 0.18, 0.05, 0.05)
        self.bombs_label = self.construct_show_amount_of_bombs_label(self.root, 0.5, 0.02, 0.05, 0.05)
        self.time_label = self.construct_time_label(self.root, 0.4, 0.02, 0.05, 0.05)

        # call backs
        self.call_backs = []

        # variables for call backs
        self.time = S_T.TIMER
        self.cycle = self.time * S_T.CLEAR_CYCLE
        self.seconds = 0
        self.update_time()
        self.cycle_call_backs()

        self.row = rows
        self.col = columns

        # marked bombs
        self.marked_bombs = []
        self.amount_of_marked_bombs = 0

        # colors
        self.color = self.colors()
        self.font = (S_T.BOARD_WIDTH * S_T.BOARD_HEIGHT) // (self.row * self.col)


    # region Graphics

    def construct_frame(self, root, r_x, r_y, r_w, r_h):
        frame = ttk.Frame(root)
        frame.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        frame.config(padding=(10, 10))
        return frame

    def construct_end_button(self, root, r_x, r_y, r_w, r_h):
        button = ttk.Button(root, text="End")
        button.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        button.config(command=self.end_game)
        return button

    def construct_restart_button(self, root, r_x, r_y, r_w, r_h):
        button = ttk.Button(root, text="Restart")
        button.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        button.config(command=self.connector.restart)
        return button

    def construct_ai_button(self, root, r_x, r_y, r_w, r_h):
        button = ttk.Button(root, text="AI")
        button.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        button.config(command=self.connector.brain_play)
        return button

    def construct_show_amount_of_bombs_label(self, root, r_x, r_y, r_w, r_h):
        label = ttk.Label(root, text="Bombs X  " + str(S_T.AMOUNT_OF_BOMBS))
        label.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        return label

    def construct_time_label(self, root, r_x, r_y, r_w, r_h):
        label = ttk.Label(root, text="Seconds: ")
        label.place(relx=r_x, rely=r_y, relwidth=r_w, relheight=r_h)
        return label

    def colors(self):
        dt = {
            -1: C_V.EMPTY_LABEL_COLOR_CHECKED,
            0: C_V.EMPTY_LABEL_COLOR_UNCHECKED,
            1: C_V.ONE_BOMB,
            2: C_V.TWO_BOMB,
            3: C_V.THREE_BOMB,
            4: C_V.FOUR_BOMB,
            5: C_V.FIVE_BOMB,
            6: C_V.SIX_BOMB,
            7: C_V.SEVEN_BOMB,
            8: C_V.EIGHT_BOMB,
            9: C_V.MARKED_BOMB,
            10: C_V.EXPOSE_BOMB,
            11: C_V.HOVER_LABEL_COLOR
        }
        return dt

    # endregion

    # region Events

    def hover_on(self, event):
        row, col = self.retrieve_label_location(event)
        hover_label = self.board[row][col]
        value = self.connector.model.board[row][col]

        if value == 0 or value == 9:
            hover_label.config(background=self.color[11])

    def hover_off(self, event):
        row, col = self.retrieve_label_location(event)
        hover_label = self.board[row][col]
        value = self.connector.model.board[row][col]

        if value == 0 or value == 9:
            hover_label.config(background=self.color[0])

    def action_right_click(self, event):

        row, col = self.retrieve_label_location(event)
        updates = self.connector.play(row, col)
        self.update_labels(updates)

    def action_left_click(self, event):

        row, col = self.retrieve_label_location(event)
        cur_label = self.board[row][col]

        if self.connector.mark_bomb(row, col):

            if [row, col] not in self.marked_bombs: # marking

                self.mark_bomb(row, col)

                cur_label.unbind("<Enter>")  # hover on
                cur_label.unbind("<Leave>")  # hover off

                # check if we marked all the bombs, if so checks if all the positions match the marked positions
                self.update_if_all_marked_bombs_right()

            else: # unmarking

                self.marked_bombs.remove([row, col])
                self.update_labels([[row, col, 0]])
                self.amount_of_marked_bombs -= 1
                self.bombs_label.config(text="Bombs X  " + str(S_T.AMOUNT_OF_BOMBS - self.amount_of_marked_bombs))
                cur_label.config(background=self.color[11])
                cur_label.bind("<Enter>", self.hover_on)  # hover on
                cur_label.bind("<Leave>", self.hover_off)  # hover off

    # endregion

    # region Methods

    def create_board(self, root, rows, columns):
        board = []
        r_y = 1 / rows
        r_x = 1 / columns
        r_w = r_x * 0.8
        r_h = r_y * 0.8
        color = C_V.EMPTY_LABEL_COLOR_UNCHECKED

        # Batch creation and placement of labels
        labels = [
            [
                ttk.Label(root, background=color, anchor=CENTER)
                for _ in range(columns)
            ]
            for _ in range(rows)
        ]

        # Place labels and bind events in a single loop
        for y in range(rows):
            row_of_labels = []
            for x in range(columns):
                label = labels[y][x]
                label.place(relx=r_x * x, rely=r_y * y, relwidth=r_w, relheight=r_h)
                self.bind_all(label)  # Consider if this can be moved outside depending on context
                row_of_labels.append(label)
            board.append(row_of_labels)

        return board

    def retrieve_label_location(self, event):

        value = str(event.widget)[14:]

        if value != "":
            return (int(value)-1) // self.col, (int(value)-1) % self.col
        else:
            return 0, 0

    def update_labels(self, updates):

        for update in updates:

            cur_label = self.board[update[0]][update[1]]
            value = update[2]

            cur_label.config(background=self.color[value])

            if 0 < value <= 8:
                cur_label.config(font=self.font, text=update[2])
                self.unbind_all(cur_label)
            else:
                cur_label.unbind("<Enter>")  # hover on
                cur_label.unbind("<Leave>")  # hover off

    def show_text(self, updates):
        for update in updates:
            cur_label = self.board[update[0]][update[1]]
            value = update[2]
            cur_label.config(font=self.font, text=value)

    def update_if_all_marked_bombs_right(self):

        # check if we marked all the bombs, if so checks if all the positions match the marked positions
        if S_T.AMOUNT_OF_BOMBS == self.amount_of_marked_bombs:
            if self.connector.check_if_found_all_bombs(self.marked_bombs):
                self.case_reveal()
                print("You Won!\nCongratulations")
                self.bombs_label.config(text="You won!")
            else:
                print("Incorrect")

    def case_reveal(self):
        self.expose_bombs()
        self.freeze_board()

    def freeze_board(self):
        for i in range(self.row):
            for j in range(self.col):
                cur_value = self.connector.model.board[i][j]
                cur_label = self.board[i][j]
                if [i, j] in self.marked_bombs:
                    cur_label.unbind("<Button-1>")
                    cur_label.unbind("<Button-3>")
                elif cur_value <= 0 or cur_value >= 9:
                    self.unbind_all(cur_label)

    def mark_bomb(self, row, col):
        self.marked_bombs.append([row, col])
        self.update_labels([[row, col, 9]])
        self.amount_of_marked_bombs += 1
        self.bombs_label.config(text="Bombs X  " + str(S_T.AMOUNT_OF_BOMBS - self.amount_of_marked_bombs))

    def expose_bombs(self):
        bomb_places = self.connector.model.bomb_places
        for bomb_place in bomb_places:
            self.board[bomb_place[0]][bomb_place[1]].config(background=self.color[10])

    def clean_probabilities_from_assured_empty_places(self, empty_places):
        for empty_place in empty_places:
            self.board[empty_place[0]][empty_place[1]].config(text="")

    def bind_all(self, cur_label):
        cur_label.bind("<Enter>", self.hover_on) # hover on
        cur_label.bind("<Leave>", self.hover_off) # hover off
        cur_label.bind("<Button-1>", self.action_right_click) # right click
        cur_label.bind("<Button-3>", self.action_left_click) # left click

    def unbind_all(self, cur_label):
        cur_label.unbind("<Enter>")
        cur_label.unbind("<Leave>")
        cur_label.unbind("<Button-1>")
        cur_label.unbind("<Button-3>")

    def end_game(self):
        self.root.destroy()

    # endregion

    # region Call Backs

    def update_time(self):

        call_back_id = self.root.after(self.time, self.update_time_call_back)
        self.call_backs.append(call_back_id)

    def update_time_call_back(self):

        self.seconds += 1
        current_time = self.seconds

        # Update the label with the current time
        self.time_label.config(text="Seconds: " + str(current_time))

        # Schedule the update_time function to be called after 1000 milliseconds (1 second)
        self.update_time()

    def cycle_call_backs(self): # used to clear call backs from the system on repeat (based on the value of self.cycle)
        call_back_id = self.root.after(self.cycle, self.clear_call_backs_call_back)
        self.call_backs.append(call_back_id)

    def clear_call_backs_call_back(self): # call the clearing of all call backs and recalling the call backs
        self.close_call_backs()
        self.recall_call_backs()

    def recall_call_backs(self): # recalling call backs
        self.cycle_call_backs()
        self.update_time()

    # end all call backs
    def close_call_backs(self):
        for call_back in self.call_backs[:]:
            try:
                self.root.after_cancel(call_back)
                self.call_backs.remove(call_back)
            except tk.TclError:
                pass

    # endregion