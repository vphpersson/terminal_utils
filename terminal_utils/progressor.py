from __future__ import annotations
from shutil import get_terminal_size
from sys import stderr


class Progressor:
    def __init__(self, fill_character: str = '█'):
        self.fill_character: str = fill_character

    def __enter__(self) -> Progressor:
        return self

    def __exit__(self, _, __, ___):
        self.print_progress_message('')

    @staticmethod
    def print_message(message: str, **print_options) -> None:
        """
        Print a message in the context of the progress, making a new line.

        :param message: The message to print.
        :param print_options: Options passed to `print`.
        :return: None
        """

        # The characters of the previous message are removed by writing whitespace for the full width of the terminal.
        print(f'{" " * get_terminal_size().columns}\r{message}', **print_options)

    @staticmethod
    def print_progress_message(message: str, prefix: str = '') -> None:
        """
        Print a message in the context of the progress, replacing the current progress line.

        :param message: The message to print.
        :param prefix: A prefix to the message.
        :return: None
        """

        Progressor.print_message(f'{prefix}{message}', end='\r', file=stderr)

    def print_progress(self, iteration: int, total: int, prefix: str = '') -> None:
        """
        Print a progress bar.

        :param iteration: The current number of processed items.
        :param total: The total number of items to process.
        :param prefix: A message to prefix the progress bar.
        :return: None
        """

        percent = f'{100 * (iteration / float(total)): 5.1f}'

        def make_progress_message(bar: str) -> str:
            return f'{prefix}[{iteration:0{len(str(total))}}/{total}] |{bar}| {percent}%'

        # The bar is to fill up the terminal width. Ascertain the length by producing a message with an empty bar, and
        # use the difference between the length of the message and the width of the terminal.
        bar_length = get_terminal_size().columns - len(make_progress_message(bar=''))
        # Ascertain how much of the bar is to be filled with the fill character.
        num_fill_characters = int((iteration / total) * bar_length)

        Progressor.print_progress_message(
            message=make_progress_message(
                bar=f'{num_fill_characters * self.fill_character}{"-" * (bar_length - num_fill_characters)}'
            )
        )


