
from enum import IntEnum


class PrintColor(IntEnum):
    DEFAULT_FOREGROUND_COLOR = 39
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    LIGHT_GRAY = 37
    DARK_GRAY = 90
    LIGHT_RED = 91
    LIGHT_GREEN = 92
    LIGHT_YELLOW = 93
    LIGHT_BLUE = 94
    LIGHT_MAGENTA = 95
    LIGHT_CYAN = 96
    WHITE = 97


class ColoredOutput:
    def __init__(self):
        self.enabled = True

    def make_color_output(self, print_color: PrintColor, message: str) -> str:
        return f'\x1b[{print_color.value}m{message}\033[0m' if self.enabled else message
