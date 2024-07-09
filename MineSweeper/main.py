from connector import *
from values import *
from tkinter import *


class Start(object):

    def __init__(self):

        self.root = ""
        self.controller = ""

        self.start()

    def start(self):

        self.root = Tk()
        self.root.title("Mine Sweeper")
        self.root.geometry(str(S_T.WIDTH)+"x"+str(S_T.HEIGHT))
        self.root.resizable(0, 0)
        self.root['bg'] = C_V.PAGE_COLOR

        self.controller = Connector(S_T.BOARD_WIDTH, S_T.BOARD_HEIGHT, self.root, self)

        self.root.bind('<Control-e>', lambda event: self.root.destroy()) # Exit
        self.root.bind('<Control-r>', lambda event: self.restart())  # Restart

        self.root.mainloop()


    def restart(self):

        self.controller.close_call_backs()
        self.root.destroy()
        self.start()


def main():

    start = Start()




if __name__ == '__main__':
    main()