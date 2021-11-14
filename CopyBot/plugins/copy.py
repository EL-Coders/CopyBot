from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from PyroBot import CHANNEL, GROUP, TO_CHANNEL, TO_GROUP



channel = int(CHANNEL)
from_group = int(GROUP)
to_channel = int(TO_CHANNEL)
to_group = int(TO_GROUP)


# from_group = int(GROUP)
# print(from_group)
@Client.on_message(filters.group & filters.chat(from_group))
async def group_saver(client, message):
    try:
        await Client.copy_message(client, chat_id=to_group, from_chat_id=from_group, message_id=message.message_id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 1)
        group_saver(client, message)


@Client.on_message(filters.channel & filters.chat(channel))
async def channel_saver(client, message):
    try:
        await Client.copy_message(client, chat_id=to_channel, from_chat_id=channel, message_id=message.message_id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 1)
        channel_saver(client, message)

