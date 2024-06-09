#!/usr/bin/env python
import os
import subprocess
from secrets import token_urlsafe
from telegram import ForceReply, Update
from telegram.ext import (
    AIORateLimiter,
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext.filters import COMMAND, TEXT

from lihua_telegram_bot.config import Config
from lihua_telegram_bot.i18n import _
from lihua_telegram_bot.log import logger


async def init(app: Application) -> None:
    await app.bot.set_my_short_description("已连接 | Connected")


async def stop(app: Application) -> None:
    await app.bot.set_my_short_description("已断开 | Disconnted")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    user = update.effective_user
    await update.message.reply_html(_("Hello Kitty").format(user.mention_html()))


async def system_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    os.environ["USER"] = __name__
    await update.message.reply_text(subprocess.run(("fastfetch", "-c", os.path.join(os.path.dirname(__file__), "config.jsonc")), capture_output=True).stdout.decode())


def main(args) -> None:
    logger.setLevel(args.log_level)
    config = Config(args.config)
    application = (
        Application.builder()
        .token(config.TOKEN)
        .rate_limiter(AIORateLimiter())
        .post_init(init)
        .post_stop(stop)
        .build()
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("systeminfo", system_info))
    try:
        from lihua_telegram_bot.mkcrt import tmp
    except RuntimeError:
        pass
    if config.WEBHOOK:
        application.run_webhook(
            listen=config.LHOST,
            port=config.LPOST,
            secret_token=token_urlsafe(128),
            webhook_url=f"https://{config.RHOST}:{config.RPOST}",
            key=config.WEBHOOK and os.path.join(tmp, "private.key"),
            cert=config.WEBHOOK and os.path.join(tmp, "cert.pem"),
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
