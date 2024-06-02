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
from faker import Faker

fake = Faker()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    user = update.effective_user
    await update.message.reply_html(
        _("Hi {}!").format(user.mention_html()),
        reply_markup=ForceReply(selective=True),
    )


async def fake_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    user = update.effective_user
    await update.get_bot().send_contact(
        chat_id=update.effective_chat.id,
        phone_number="+1 (145)141-9198",
        first_name=user.first_name,
        last_name=user.last_name,
    )


def main() -> None:
    app = (
        Application.builder().token(config.TOKEN).rate_limiter(AIORateLimiter()).build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fake", fake_contact))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
