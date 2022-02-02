import argparse
import datetime
import logging
import sys
from pathlib import Path

from automatictime.config import ConfigManager
from automatictime.google_sheet import GoogleSheet

log = logging.getLogger(__name__)


class CliParser:

    def __init__(self):
        self._parser = self.create_parser()

    def get_parser(self):
        return self._parser

    def create_parser(self):
        return argparse.ArgumentParser()

    def add_arguments(self):
        self._parser.add_argument("-c", "--config-dir", type=Path, default=Path.home().joinpath(".automatictime"))
        self._parser.add_argument("--begin", action="store_true")
        self._parser.add_argument("--end", action="store_true")
        self._parser.add_argument("-d", "--debug", action="store_true")

    def parse(self):
        options = self._parser.parse_args()
        return options

    def validate(self, options):
        if not Path(options.config_dir).is_dir():
            raise ValueError("-c must be a Directory")

    def handle(self, options):
        now = datetime.datetime.now()
        if len(sys.argv) == 1:
            self._parser.print_help(sys.stderr)
            sys.exit(1)

        if options.debug is True:
            logging.basicConfig(level=logging.DEBUG)
            logging.debug("Enable Debug-Mode")

        config = ConfigManager(options)

        sheet = GoogleSheet(config)
        linenr = sheet.find_line()

        time = now.strftime("%H:%M")

        if options.begin:
            sheet.update(linenr, "TOPIC", "Arbeit")
            sheet.update(linenr, "START", time)

        if options.end:
            sheet.update(linenr, "TOPIC", "Arbeit")
            sheet.update(linenr, "END", time)

    @staticmethod
    def initialize():
        parser = CliParser()
        parser.add_arguments()
        options = parser.parse()
        parser.validate(options)
        parser.handle(options)


if __name__ == "__main__":
    CliParser.initialize()
