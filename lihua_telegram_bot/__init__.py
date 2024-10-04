from telegram import (
    Chat,
    ForumTopic,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyParameters,
    TextQuote,
    Update,
)
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not context.user_data.get("-1002325071906"):
        topic: ForumTopic = await context.bot.create_forum_topic(
            -1002325071906, str(user.id)
        )

        context.user_data["-1002325071906"] = topic.message_thread_id
        context.bot_data[f"-1002325071906_{topic.message_thread_id}"] = user.id
        msg: Message = await context.bot.send_message(
            -1002325071906,
            user.mention_markdown_v2(),
            ParseMode.MARKDOWN_V2,
            message_thread_id=topic.message_thread_id,
        )
        await msg.pin()


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != -1002325071906:
        return
    msg: Message = update.effective_message
    reply: Message = msg.reply_to_message
    if not reply:
        target: Message = await msg.copy(msg.forum_topic_created.name)
    elif reply.reply_markup:
        _, uid, mid = reply.reply_markup.inline_keyboard[0][0].callback_data.split("_")
        quote: TextQuote = msg.quote
        target: Message = await msg.copy(
            uid, reply_parameters=ReplyParameters(mid, quote=quote and quote.text)
        )
    elif reply.forum_topic_created:
        target: Message = await msg.copy(reply.forum_topic_created.name)
    else:
        quote: TextQuote = msg.quote
        target: Message = await msg.copy(
            context.bot_data[f"{reply.chat.id}_{reply.message_thread_id}"],
            reply_parameters=ReplyParameters(
                context.chat_data[str(reply.message_id)], quote=quote and quote.text
            ),
        )
    context.chat_data[str(msg.message_id)] = target.message_id


async def sync2chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    await context.bot.delete_message(uid, mid)
