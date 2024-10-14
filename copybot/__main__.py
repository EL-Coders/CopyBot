import uvloop

uvloop.install()

import asyncio

from pyrogram import Client, __version__, idle  # noqa: E402
from pyrogram.raw.all import layer  # noqa: E402

from copybot import API_HASH, APP_ID, BOT_TOKEN, SESSION

bot = None
user = None


async def main():
    global bot, user
    plugins = dict(root="copybot/plugins")
    bot = Client(
        name="copybot",
        api_id=APP_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=plugins,
    )
    if SESSION:
        user = Client(
            name="user_copybot",
            api_id=APP_ID,
            api_hash=API_HASH,
            session_string=SESSION,
            plugins=plugins,
        )
    async with bot:
        print(
            f"{bot.me.first_name} - @{bot.me.username} - Pyrogram v{__version__} (Layer {layer}) - Bot Started..."
        )
        if user:
            await user.start()
            print(
                f"{user.me.first_name} - @{user.me.username} - Pyrogram v{__version__} (Layer {layer}) - User Started..."
            )

        await idle()

        print(f"{bot.me.first_name} - @{bot.me.username} - Bot Stopped !!!")
        if user:
            await user.stop()
            print(f"{user.me.first_name} - @{user.me.username}- User Stopped !!!")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
