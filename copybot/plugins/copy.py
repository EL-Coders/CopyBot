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

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from copybot.db.db import get_dest_by_source, get_source_channels

SOURCE_CHATS = []
file_groups = []


async def get_source():
    global SOURCE_CHATS
    while True:
        SOURCE_CHATS = await get_source_channels()
        await asyncio.sleep(60)


@Client.on_message((filters.group | filters.channel), group=1)
async def file_copier(bot, message):
    curr_chat = message.chat.id
    if curr_chat in SOURCE_CHATS:
        dest_chats = await get_dest_by_source(curr_chat)
        for chat in dest_chats:
            if message.media_group_id:
                if message.media_group_id in file_groups:
                    return
                file_groups.append(message.media_group_id)
                messages = await message.get_media_group()
                for mess in messages:
                    await copy_message(mess, chat)
            else:
                await copy_message(message, chat)


async def copy_message(message, chat_id):
    try:
        await message.copy(chat_id)
    except FloodWait as e:
        await asyncio.sleep(e.value + 1)
        await copy_message(message, chat_id)


loop = asyncio.get_event_loop()
loop.create_task(get_source())
