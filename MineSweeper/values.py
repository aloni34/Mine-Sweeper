class SettingValues(object):

    def __init__(self):

        self.HEIGHT = 1080
        self.WIDTH = 1920

        self.BOARD_HEIGHT = 30
        self.BOARD_WIDTH = 30

        self.AMOUNT_OF_BOMBS = 99

        self.TIMER = 1000  # milliseconds
        self.CLEAR_CYCLE = 1800  # Used to avoid huge quantity of call backs. Set to be every 30 minutes
        self.DELAY_MODIFIER = 0.05  # seconds


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
