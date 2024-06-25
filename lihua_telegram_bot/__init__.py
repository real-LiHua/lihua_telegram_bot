#!/usr/bin/env python
import os
import subprocess
from base64 import b64encode
from secrets import token_urlsafe
from hashlib import md5

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
    await app.bot.set_my_commands(
        [
            ("start", _("开始")),
            ("lmstfy", _("让我帮你搜索一下")),
            ("id", _("获取ID")),
            ("apatch", _("获取apatch群组密码")),
            ("kernelsu", _("获取kernelsu群组密码")),
            ("systeminfo", _("系统信息")),
        ]
    )


async def stop(app: Application) -> None:
    await app.bot.set_my_commands([])
    await app.bot.set_my_short_description("已断开 | Disconnected")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable= W0613
    await update.message.reply_html(_("Hello Kitty"))


async def system_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable= W0613
    await update.message.reply_text(
        subprocess.run(
            (
                "fastfetch",
                "-c",
                os.path.join(os.path.dirname(__file__), "config.jsonc"),
            ),
            capture_output=True,
            check=True,
        ).stdout.decode()
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.reply_to_message or update.message
    uid = msg.from_user.id
    gid = msg.chat.id
    mid = msg.message_id
    text = f"用户ID: {uid}\n"
    if uid != gid:
        text += f"群组ID: {gid}\n"
    text += f"消息ID: {mid}\n"
    await update.message.reply_text(text)

async def lmstfy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # pylint: disable= W0613
    msg = update.message
    text = msg.text
    text = text[text.find(" ") :][1:].strip()
    if not text and msg.reply_to_message:
        text = (msg.quote or msg.reply_to_message).text
    v = b64encode(text.encode()).decode().rstrip("=")
    await (msg.reply_to_message or msg).reply_text(f"https://lmstfy.net/?q={v}")


async def apatch(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id=update.message.from_user.id
    sign = md5(f'{user_id}apatch'.encode('utf-8')).hexdigest()
    await update.message.reply_text(sign)

async def kernelsu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("没写")

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
    application.add_handler(CommandHandler("lmstfy", lmstfy))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("apatch", apatch))
    application.add_handler(CommandHandler("kernelsu", kernelsu))
    application.add_handler(CommandHandler("systeminfo", system_info))
    application.add_handler(CommandHandler("start", start))

    if int(config.WEBHOOK) and not __debug__:
        try:
            # pylint:disable=C0415
            from lihua_telegram_bot.mkcrt import tmp
        except RuntimeError:
            pass
        application.run_webhook(
            listen=config.LHOST,
            port=config.LPOST,
            secret_token=token_urlsafe(128),
            webhook_url=f"https://{config.RHOST}:{config.RPOST}",
            key=os.path.join(tmp, "private.key"),
            cert=os.path.join(tmp, "cert.pem"),
        )
    else:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
