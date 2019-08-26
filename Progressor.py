from shutil import get_terminal_size
from typing import Union, IO, Optional
from sys import stderr, stdout


class Progressor:
    def __init__(self, bar_length: int = 50, fill_character: str = '█'):
        self.bar_length = bar_length
        self.fill_character = fill_character

        self._last_message_length = 0

    def print_message(self, message: str, end: Optional[str] = '\n', file: Optional[IO] = stdout) -> None:

        message_len = len(message)

        print(f'\r{message}{" " * max(0, self._last_message_length - message_len)}', end=end, file=file)

        self._last_message_length = message_len

    def print_progress_message(self, message: str, prefix: str = '') -> None:
        self.print_message(f'{prefix}{message}', end='\r', file=stderr)

    def print_progress(self, iteration: int, total: int, prefix: str = '', suffix: str = '') -> None:
        """Print a progress bar."""

        percent = f'{100 * (iteration / float(total)): 5.1f}'

        def gen_msg(bar: str = '') -> str:
            return f'{prefix}[{iteration:0{len(str(total))}}/{total}] |{bar}| {percent}%'

        bar_length = get_terminal_size().columns - len(gen_msg())

        filled_length = int((iteration / total) * bar_length)
        bar = f'{self.fill_character * filled_length}{"-" * (bar_length - filled_length)}'

        self.print_progress_message(gen_msg(bar))
