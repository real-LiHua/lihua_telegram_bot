#!/usr/bin/env python
import os
import subprocess
from base64 import b64encode
from hashlib import md5
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
    await app.bot.set_my_commands(
        [
            ("start", _("开始")),
            ("lmstfy", _("让我帮你搜索一下")),
            ("id", _("获取ID")),
            ("encrypt", _("加密")),
            ("decrypt", _("解密")),
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
                "config.jsonc",
            ),
            check=True,
            cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).stdout.decode()
    )


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.message.reply_to_message or update.message
    uid = f"<code>{msg.from_user.id}</code>"
    gid = f"<code>{msg.chat.id}</code>"
    args = update.message.text.split()
    if len(args) > 1:
        if args[1] == "-u":
            reply = uid
        elif args[1] == "-g":
            reply = gid
    else:
        reply = (f"uid={uid}({{}}) gid={gid}({{}})").format(
            msg.from_user.mention_html(),
            (
                f"<code>{msg.chat.title}</code>"
                if msg.chat.title
                else msg.from_user.mention_html()
            ),
        )
    await update.message.reply_html(reply)


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
    user_id = update.message.from_user.id
    sign = md5(f"{user_id}apatch".encode("utf-8")).hexdigest()
    await update.message.reply_text(sign)


async def kernelsu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.split()
    if len(text) != 2:
        return
    await update.message.reply_text(
        subprocess.run(
            ("node", "xxtea.js", text[1], "114514"),
            cwd=os.path.dirname(__file__),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).stdout.decode()
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
