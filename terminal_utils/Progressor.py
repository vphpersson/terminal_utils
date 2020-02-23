from __future__ import annotations
from shutil import get_terminal_size
from typing import IO, Optional
from sys import stderr, stdout


class Progressor:
    def __init__(self, fill_character: str = '█'):
        self.fill_character = fill_character
        self._last_message_length = 0

    def __enter__(self) -> Progressor:
        return self

    def __exit__(self, _, __, ___):
        self.print_progress_message('')

    def print_message(self, message: str, end: Optional[str] = '\n', file: Optional[IO] = stdout) -> None:
        """
        Print a message in the context of the progress, making a new line.

        :param message: The message to print.
        :param end:
        :param file: The
        :return: None
        """

        message_len = len(message)

        print(f'\r{message}{" " * max(0, self._last_message_length - message_len)}', end=end, file=file)

        self._last_message_length = message_len

    def print_progress_message(self, message: str, prefix: str = '') -> None:
        """
        Print a message in the context of the progress, replacing the current progress line.

        :param message: The message to print.
        :param prefix: A prefix to the message.
        :return: None
        """

        self.print_message(f'{prefix}{message}', end='\r', file=stderr)

    def print_progress(self, iteration: int, total: int, prefix: str = '') -> None:
        """
        Print a progress bar.

        :param iteration: The current number of processed items.
        :param total: The total number of items to process.
        :param prefix: A message to prefix the progress bar.
        :return: None
        """

        percent = f'{100 * (iteration / float(total)): 5.1f}'

        def gen_msg(bar: str = '') -> str:
            return f'{prefix}[{iteration:0{len(str(total))}}/{total}] |{bar}| {percent}%'

        bar_length = get_terminal_size().columns - len(gen_msg())

        filled_length = int((iteration / total) * bar_length)
        bar = f'{self.fill_character * filled_length}{"-" * (bar_length - filled_length)}'

        self.print_progress_message(gen_msg(bar))
