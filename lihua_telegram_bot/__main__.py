import argparse
import sys

from lihua_telegram_bot import main
from lihua_telegram_bot.i18n import _

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", help=_("config file"))
parser.add_argument(
    "-l",
    "--log-level",
    choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    help=_("log level"),
)
sys.exit(main(parser.parse_args()))
