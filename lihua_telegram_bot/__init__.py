from telegram import (
    Chat,
    ForumTopic,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.user_data.get(str(user.id)):
        topic: ForumTopic = await context.bot.create_forum_topic(
            -1002325071906, str(user.id)
        )

        context.user_data["-1002325071906"] = topic.message_thread_id

        msg: Message = await context.bot.send_message(
            -1002325071906,
            "User: {}\nUser ID: {}".format(user.mention_markdown_v2(), user.id),
            ParseMode.MARKDOWN_V2,
            message_thread_id=topic.message_thread_id,
        )
        await msg.pin()


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.copy(
        -1002325071906,
        message_thread_id=context.user_data["-1002325071906"],
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "DELETE",
                        callback_data="DELETE_{}_{}".format(
                            update.effective_user.id,
                            update.effective_message.message_id,
                        ),
                    )
                ]
            ]
        ),
    )


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    _, uid, mid = query.data.split("_")
    await context.bot.delete_message(uid, str(mid))
