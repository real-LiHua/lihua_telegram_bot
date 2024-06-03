#!/usr/bin/env python
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

from lihua_telegram_bot import config
from lihua_telegram_bot.i18n import _
from lihua_telegram_bot.log import log
from lihua_telegram_bot.mkcrt import tmp


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


def main() -> None:
    application = (
        Application.builder()
        .token(config.TOKEN)
        .rate_limiter(AIORateLimiter())
        .post_init(init)
        .post_stop(stop)
        .build()
    )
    application.add_handler(CommandHandler("start", start))
    application.run_webhook(
        listen="::",
        port=8443,
        secret_token=token_urlsafe(128),
        webhook_url=f"https://{config.IP}:8443",
        key=f"{tmp}/private.key",
        cert=f"{tmp}/cert.pem",
    )
