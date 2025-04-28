import machine  # type: ignore
from aalec import constants
from aalec.third_party import sh1106


class Display:
    """Display class.

    Args:
        i2c: A `machine.I2C` instance.
    """

    def __init__(self, i2c: machine.I2C):
        self._display = sh1106.SH1106_I2C(
            constants.DISPLAY_WIDTH, constants.DISPLAY_HEIGHT, i2c
        )
        self._display.rotate()

    def print_line(self, line: int, text: str) -> None:
        """Print a line of text on the display.

        A line can be at most 16 characters long. (A character has a size of 8x8 pixels.)

        Args:
            line (int): Line number. Valid values are from 1 to 5.
            text (str): The content to display.
        """
        y = ((line - 1) % constants.MAX_LINE_COUNT) * constants.LINE_HEIGHT
        self._display.fill_rect(
            0,
            y,
            constants.DISPLAY_WIDTH,
            constants.LINE_HEIGHT,
            constants.BLACK,
        )
        self._display.text(text, 0, y)
        self._display.show()
        pass

    def clear_display(self) -> None:
        """Clear the display."""
        self._display.fill(constants.BLACK)
        self._display.show()

    def rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draw a rectangle frame on the display.

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            color (int): Frame color (`constants.WHITE` or `constants.BLACK`)
        """
        self._display.rect(x, y, width, height, color)
        self._display.show()

    def filled_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Draw a filled rectangle on the display.

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            color (int): Fill color (`constants.WHITE` or `constants.BLACK`)
        """
        self._display.fill_rect(x, y, width, height, color)
        self._display.show()

    def draw_progressbar(
        self, x: int, y: int, width: int, height: int, percent: int
    ) -> None:
        """Draw a progressbar.

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            percent (int): How many percent the bar is filled (grows to the right).
        """
        # Blank the space for the progressbar.
        self._display.fill_rect(x, y, width, height, constants.BLACK)
        # Draw the frame
        if height >= 3:
            self._display.rect(x, y, width, height, constants.WHITE)
            inner_width = int((width - 2) * percent / 100)
            self._display.fill_rect(
                x + 1, y + 1, inner_width, height - 2, constants.WHITE
            )
        else:
            inner_width = int(width * percent / 100)
            self._display.fill_rect(x, y, inner_width, height, constants.WHITE)
        self._display.show()


def test_display() -> None:
    """Test for the display class."""
    from time import sleep

    i2c = machine.I2C(
        sda=machine.Pin(constants.PIN_SDA), scl=machine.Pin(constants.PIN_SCL)
    )
    display = Display(i2c)

    screens = [
        ["Once Once upon a", "midnight dreary,", "while I", "pondered, weak"],
        ["and weary, Over", "many a quaint", "and curious", "volume of"],
        ["forgotten lore-", "While I nodded,", "nearly napping,", "suddenly there"],
        ["came a tapping,", "As of some one", "gently rapping,", "rapping at my"],
        ["chamber door.", '"Tis some', 'visitor," I', "muttered,"],
        ['"tapping at my', "chamber door-", "Only this and", "nothing more."],
    ]
    screen_count = len(screens)

    for nr, screen in enumerate(screens):
        display.filled_rect(0, 0, 128, 59, constants.BLACK)
        for lnr, line in enumerate(screen):
            display.print_line(lnr + 1, line)
            display.draw_progressbar(
                0, 60, 100, 3, int((4 * nr + lnr + 1) * 100.0 / (4 * screen_count))
            )
            sleep(1)
