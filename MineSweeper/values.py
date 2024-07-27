class SettingValues(object):

    def __init__(self):

        self.HEIGHT = 1080
        self.WIDTH = 1920

        self.BOARD_HEIGHT = 30
        self.BOARD_WIDTH = 30

        self.AMOUNT_OF_BOMBS = 158

        self.TIMER = 1000  # milliseconds
        self.CLEAR_CYCLE = 1800  # Used to avoid huge quantity of call backs. Set to be every 30 minutes
        self.DELAY_MODIFIER = 0  # milliseconds

        self.IS_TO_SAVE = False  # save the data in a file
        self.NUMBER_OF_TESTS = 3000  # amount of tests for the test class to create (collect data) (0 - no tests)
        self.TEST_CYCLE = 1  # amount of repeats of the number of tests (self.NUMBER_OF_TESTS)
        self.STEP = 0  # amount of bombs to add or remove each new iteration of the repetition (self.TEST_CYCLE)


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
        self.EIGHT_BOMB = "Cyan"
        self.MARKED_BOMB = "Cyan"
        self.EXPOSE_BOMB = "BLACK"
        self.HOVER_LABEL_COLOR = "lavender"


S_T = SettingValues()
C_V = ConstantValues()
