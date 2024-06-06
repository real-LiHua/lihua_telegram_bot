#!/usr/bin/env python
import os.path
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
    await app.bot.set_my_short_description("Connected")


async def stop(app: Application) -> None:
    await app.bot.set_my_short_description("Disconnected")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    user = update.effective_user
    await update.message.reply_html(
        _("Hi {}!").format(user.mention_html()),
        reply_markup=ForceReply(selective=True),
    )


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
    try:
        from lihua_telegram_bot.mkcrt import tmp
    except RuntimeError:
        pass
    application.run_webhook(
        listen=config.LHOST,
        port=config.LPOST,
        secret_token=token_urlsafe(128),
        webhook_url=f"https://{config.RHOST}:{config.RPOST}",
        key=os.path.join(tmp, "private.key") if config.SSL else None,
        cert=os.path.join(tmp, "cert.pem") if config.SSL else None,
    )
