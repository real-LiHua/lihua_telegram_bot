#!/usr/bin/env python
from telegram import ForceReply, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler)
from telegram.ext.filters import COMMAND, TEXT

from lihua_telegram_bot import config
from lihua_telegram_bot.i18n import _
from lihua_telegram_bot.log import log


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=E0602,W0613
    user = update.effective_user
    await update.message.reply_html(
        _("Hi {}!").format(user.mention_html()),
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    await update.message.reply_text(_("Help!"))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable=W0613
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = Application.builder().token(config.TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(TEXT & ~COMMAND, echo))
    app.run_polling(allowed_updates=Update.ALL_TYPES)
