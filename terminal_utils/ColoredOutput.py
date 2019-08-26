
from enum import IntEnum


class PrintColor(IntEnum):
    GREEN = 32
    YELLOW = 33
    RED = 91


class ColoredOutput:
    def __init__(self):
        self.enabled = True

        self._yellow_color_wrapper = ColoredOutput.get_color_wrapper(PrintColor.YELLOW)
        self._green_color_wrapper = ColoredOutput.get_color_wrapper(PrintColor.GREEN)
        self._red_color_wrapper = ColoredOutput.get_color_wrapper(PrintColor.RED)

    def print_yellow(self, message: str) -> str:
        return self._yellow_color_wrapper(message) if self.enabled else message

    def print_green(self, message: str) -> str:
        return self._green_color_wrapper(message) if self.enabled else message

    def print_red(self, message: str) -> str:
        return self._red_color_wrapper(message) if self.enabled else message

    @staticmethod
    def get_color_wrapper(color_code: int):
        return lambda s: f'\x1b[{color_code}m{s}\033[0m'
