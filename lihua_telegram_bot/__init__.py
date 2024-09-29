from telegram import ForumTopic, Message, Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_chat
    if not context.user_data.get(str(user.id)):
        topic: ForumTopic = await context.bot.create_forum_topic(
            -1002325071906, str(user.id)
        )
        context.user_data[str(user.id)] = topic.message_thread_id
        msg: Message = await context.bot.send_message(
            -1002325071906,
            "User: {}\nUser ID: {}".format(user.mention_markdown_v2(), user.id),
            ParseMode.MARKDOWN_V2,
            message_thread_id=topic.message_thread_id,
        )
        await msg.pin()
