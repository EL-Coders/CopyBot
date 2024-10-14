# Copyright (C) 2024 @jithumon
#
# This file is part of copybot.
#
# copybot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# copybot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with copybot.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import os
import shutil
import sys
import time

from psutil import cpu_percent, disk_usage, virtual_memory
from pyrogram import Client, filters

from __main__ import bot
from copybot import ADMINS, LOGGER

# from pyrogram.types import LinkPreviewOptions
from copybot.utils.util_support import humanbytes  # , get_db_size, is_admin


@bot.on_callback_query(filters.regex(r"^start_cb$"))
@bot.on_message(filters.command(["start"]) & filters.private)
async def start(bot, update):
    await update.reply_text("Hi, I am a premium file forwarder bot")


@bot.on_callback_query(filters.regex(r"^help_cb$"))
@bot.on_message(filters.command(["help"]))
async def help_m(bot, message):
    help_msg = """
/addchat - Add chat to source and destination - `/addchat SOURCE_CHAT_ID DEST_CHAT_ID`
__eg: /addchat -10012345111 -100123456112__
/delchat - Remove chat from source and destination - `/delchat SOURCE_CHAT_ID DEST_CHAT_ID`
__eg: /delchat -10012345111 -100123456112__
/listallchats - List all active chats.
    """
    await message.reply_text(help_msg)


@bot.on_message(filters.command(["restart"]) & filters.user(ADMINS))
async def restart(bot, update):
    LOGGER.warning("Restarting bot using /restart command")
    msg = await update.reply_text(text="__Restarting.....__", quote=True)
    await asyncio.sleep(5)
    await msg.edit("__Bot restarted !__")
    os.execv(sys.executable, ["python3", "-m", "copybot"] + sys.argv)


@bot.on_message(filters.command(["logs"]) & filters.user(ADMINS))
async def log_file(bot, update):
    logs_msg = await update.reply("__Sending logs, please wait...__", quote=True)
    try:
        await update.reply_document("logs.txt")
    except Exception as e:
        await update.reply(str(e))
    await logs_msg.delete()


@bot.on_message(filters.command(["server"]) & filters.user(ADMINS))
async def server_stats(bot, update):
    sts = await update.reply_text("__Calculating, please wait...__", quote=True)
    total, used, free = shutil.disk_usage(".")
    ram = virtual_memory()
    start_t = time.time()
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000

    ping = f"{time_taken_s:.3f} ms"
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    t_ram = humanbytes(ram.total)
    u_ram = humanbytes(ram.used)
    f_ram = humanbytes(ram.available)
    cpu_usage = cpu_percent()
    ram_usage = virtual_memory().percent
    used_disk = disk_usage("/").percent
    # db_size = get_db_size()
    db_size = "SQL"

    stats_msg = f"--**BOT STATS**--\n`Ping: {ping}`\n\n--**SERVER DETAILS**--\n`Disk Total/Used/Free: {total}/{used}/{free}\nDisk usage: {used_disk}%\nRAM Total/Used/Free: {t_ram}/{u_ram}/{f_ram}\nRAM Usage: {ram_usage}%\nCPU Usage: {cpu_usage}%`\n\n--**DATABASE DETAILS**--\n`{db_size}`"
    try:
        await sts.edit(stats_msg)
    except Exception as e:
        await update.reply_text(str(e), quote=True)
