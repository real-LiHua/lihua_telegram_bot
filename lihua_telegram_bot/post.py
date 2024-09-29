from telegram.ext import Application


async def init(application: Application) -> None:
    await application.bot.set_my_commands([("start", "Starts the bot")])


async def stop(application: Application) -> None:
    await application.bot.send_message(1042436080, "Shutting down...")


async def shutdown(application: Application) -> None:
    # await application.bot_data['database'].close()
    pass
