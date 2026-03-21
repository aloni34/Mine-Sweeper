class SettingValues(object):

    def __init__(self):

        self.HEIGHT = 1080
        self.WIDTH = 1920

        self.BOARD_HEIGHT = 10
        self.BOARD_WIDTH = 10

        self.AMOUNT_OF_BOMBS = 25

        self.TIMER = 1000  # milliseconds
        self.CLEAR_CYCLE = 300  # Used to avoid huge quantity of call backs. Set to be every 5 minutes (300 seconds)
        self.DELAY_MODIFIER = 10000  # milliseconds

        self.IS_TO_SAVE = False  # save the data in a file
        self.IS_TO_LOAD = False  # if we want to play on saved maps (load file by height, width and amount of bombs)

        self.NUMBER_OF_TESTS = 10  # amount of tests for the test class to create (collect data) (0 - no tests)
        self.TEST_CYCLE = 0  # amount of repeats of the number of tests (self.NUMBER_OF_TESTS)
        self.STEP = 25  # amount of bombs to add or remove each new iteration of the repetition (self.TEST_CYCLE)

        self.IS_TO_VIEW = True  # use to turn on and off the view (can help with calculation time)


class ConstantValues(object):

    def __init__(self):

        self.PAGE_COLOR = "Black"
        self.EMPTY_LABEL_COLOR_CHECKED = "White"
        self.EMPTY_LABEL_COLOR_UNCHECKED = "Gray"
        self.ONE_BOMB = "Green"
        self.TWO_BOMB = "Yellow"
        self.THREE_BOMB = "Orange"
        self.FOUR_BOMB = "Red"
        self.FIVE_BOMB = "Purple"
        self.SIX_BOMB = "PINK"
        self.SEVEN_BOMB = "BLUE"
        self.EIGHT_BOMB = "Lime"
        self.MARKED_BOMB = "Cyan"
        self.EXPOSE_BOMB = "BLACK"
        self.HOVER_LABEL_COLOR = "lavender"


S_T = SettingValues()
C_V = ConstantValues()
