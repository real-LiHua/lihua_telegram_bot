import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path

from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    PicklePersistence,
)

from . import post, start

parser: ArgumentParser = ArgumentParser("python -m lihua_telegram_bot")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-k", "--token")
parser.add_argument("-p", "--proxy")
args: Namespace = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

if args.debug:
    logging.getLogger("telegram.ext.Application").setLevel(logging.DEBUG)

application: Application = (
    ApplicationBuilder()
    .token(args.token)
    .http_version("2")
    .persistence(PicklePersistence(filepath=Path("site") / "bot", single_file=False))
    .post_init(post.init)
    .post_stop(post.stop)
    .post_shutdown(post.shutdown)
    .proxy(args.proxy)
    .build()
)

application.add_handler(CommandHandler("start", start))
application.run_polling()
