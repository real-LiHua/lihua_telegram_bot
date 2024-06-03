#!/usr/bin/env python
from telegram import ForceReply, Update
from telegram.ext import (
    AIORateLimiter,
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext.filters import COMMAND, TEXT

from lihua_telegram_bot import config
from lihua_telegram_bot.i18n import _
from lihua_telegram_bot.log import log


async def init(app):
    await app.bot.set_my_short_description("Connected")


async def stop(app):
    await app.bot.set_my_short_description("Disconnected")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    user = update.effective_user
    await update.message.reply_html(
        _("Hi {}!").format(user.mention_html()),
        reply_markup=ForceReply(selective=True),
    )


def main() -> None:
    app = (
        Application.builder()
        .token(config.TOKEN)
        .rate_limiter(AIORateLimiter())
        .post_init(init)
        .post_stop(stop)
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
