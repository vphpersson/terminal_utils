from logging import Handler, CRITICAL, ERROR, WARNING, INFO, DEBUG, LogRecord
from typing import Optional
from dataclasses import dataclass

from terminal_utils.progressor import Progressor
from terminal_utils.colored_output import ColoredOutput, PrintColor


@dataclass
class ProgressStatus:
    iteration: int
    total: int
    prefix: Optional[str] = ''


class ProgressorLogHandler(Handler):

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


class ColoredProgressorLogHandler(ProgressorLogHandler):

    def __init__(self, progressor: Progressor, **handler_options):
        super().__init__(progressor=progressor, **handler_options)
        self._colored_output = ColoredOutput()

    def emit(self, record: LogRecord):
        if isinstance(record.msg, ProgressStatus):
            super().emit(record=record)
            return

        formatted_message: str = self.format(record=record)

        if record.levelno in {CRITICAL, ERROR}:
            self._progressor.print_message(
                message=self._colored_output.make_color_output(print_color=PrintColor.RED, message=formatted_message)
            )
        elif record.levelno == WARNING:
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
