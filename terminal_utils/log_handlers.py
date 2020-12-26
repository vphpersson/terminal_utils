from logging import Handler, CRITICAL, ERROR, WARNING, INFO, DEBUG, LogRecord
from typing import Optional
from dataclasses import dataclass
from sys import stderr

from terminal_utils.progressor import Progressor
from terminal_utils.colored_output import ColoredOutput, PrintColor


@dataclass
class ProgressStatus:
    iteration: int
    total: int
    prefix: Optional[str] = ''


class ProgressorLogHandler(Handler):
    """
    A log handler that outputs a progress bar.

    The log handler handles the special `LogRecord` of the type `ProgressStatus`, which specifies information about
    progression status and the appearance of the progress bar.
    """

    def __init__(self, progressor: Progressor, **handler_options):
        super().__init__(**handler_options)
        self._progressor: Progressor = progressor

    def emit(self, record: LogRecord) -> None:
        if not isinstance(record.msg, ProgressStatus):
            raise ValueError(f'The log message is not of the progress status type.')

        self._progressor.print_progress(
            iteration=record.msg.iteration,
            total=record.msg.total,
            prefix=record.msg.prefix
        )


class ColoredLogHandler(Handler):
    def __init__(self, **handler_options):
        super().__init__(**handler_options)
        self._colored_output = ColoredOutput()

    def emit(self, record: LogRecord) -> None:
        """
        Output a log record message in color depending the record's severity.

        The mapping between log severity and color is:
            `CRITICAL`, `ERROR`: red
            `WARNING`: yellow
            `INFO`: green
            `DEBUG`: white

        :param record: The log record to be output.
        :return: None
        """

        formatted_message: str = self.format(record=record)

        if record.levelno in {CRITICAL, ERROR}:
            print(
                self._colored_output.make_color_output(print_color=PrintColor.RED, message=formatted_message),
                file=stderr
            )
        elif record.levelno == WARNING:
            print(
                self._colored_output.make_color_output(print_color=PrintColor.YELLOW, message=formatted_message),
                file=stderr
            )
        elif record.levelno == INFO:
            print(
                self._colored_output.make_color_output(print_color=PrintColor.GREEN, message=formatted_message),
                file=stderr
            )
        elif record.levelno == DEBUG:
            print(
                self._colored_output.make_color_output(print_color=PrintColor.WHITE, message=formatted_message),
                file=stderr
            )
        else:
            raise ValueError(f'Unknown log level: levelno={record.levelno}')


class ColoredProgressorLogHandler(ProgressorLogHandler, ColoredLogHandler):
    """A log handler that outputs log records of different severity in different colors, or outputs a progress bar."""

    def __init__(self, progressor: Progressor, print_warnings: bool = True, **handler_options):
        """
        Instantiate a `ColoredProgressorLogHandler``.

        Regarding `print_warnings`: if one wants to not print log messages having the `WARNING` severity but still see
        the progress bar, it does not work to set the log level of the handler to `ERROR`, as the progress bar is output
        via log messages having the `DEBUG` severity. Thus, there must be an extra option for this scenario.

        :param progressor: The progressor with which to output the log messages.
        :param print_warnings: Whether to not print log messages having the `WARNING` severity.
        :param handler_options: Options passed to the `argparse.Handler` superclass.
        """

        super().__init__(progressor=progressor, **handler_options)
        self._colored_output = ColoredOutput()
        self.print_warnings = print_warnings

    def emit(self, record: LogRecord) -> None:
        """
        Forward a log record to the `ProgressorLogHandler` superclass or output the record a colored message.

        The mapping between log severity and color is:
            `CRITICAL`, `ERROR`: red
            `WARNING`: yellow
            `INFO`: green
            `DEBUG`: white

        :param record: The log record to be output.
        :return: None
        """

        if isinstance(record.msg, ProgressStatus):
            super().emit(record=record)
            return

        formatted_message: str = self.format(record=record)

        if record.levelno in {CRITICAL, ERROR}:
            self._progressor.print_message(
                message=self._colored_output.make_color_output(print_color=PrintColor.RED, message=formatted_message)
            )
        elif record.levelno == WARNING:
            if self.print_warnings:
                self._progressor.print_message(
                    message=self._colored_output.make_color_output(print_color=PrintColor.YELLOW, message=formatted_message)
                )
        elif record.levelno == INFO:
            self._progressor.print_message(
                message=self._colored_output.make_color_output(print_color=PrintColor.GREEN, message=formatted_message)
            )
        elif record.levelno == DEBUG:
            self._progressor.print_message(
                message=self._colored_output.make_color_output(print_color=PrintColor.WHITE, message=formatted_message)
            )
        else:
            raise ValueError(f'Unknown log level: levelno={record.levelno}')
