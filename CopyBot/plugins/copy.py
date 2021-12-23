from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from CopyBot import CHANNEL, GROUP, TO_CHANNEL, TO_GROUP



channel = int(CHANNEL)
from_group = int(GROUP)
to_channel = int(TO_CHANNEL)
to_group = int(TO_GROUP)
file_groups = []


# from_group = int(GROUP)
# print(from_group)
@Client.on_message(filters.group & filters.chat(from_group))
async def group_saver(client, message):
    global file_groups
    if message.media_group_id:
        if message.media_group_id in file_groups:
            return
        else:
            file_groups.append(message.media_group_id)

        messages = await message.get_media_group()
        for message in messages:
            await copy_message(message, to_group)
    else:
        await copy_message(message, to_group)


@Client.on_message(filters.channel & filters.chat(channel))
async def channel_saver(client, message):
    global file_groups
    if message.media_group_id:
        if message.media_group_id in file_groups:
            return
        else:
            file_groups.append(message.media_group_id)

        messages = await message.get_media_group()
    for message in messages:
            await copy_message(message, to_channel)
    else:
        await copy_message(message, to_channel)


async def copy_message(message, chat_id):
    try:
        await message.copy(chat_id)
    except FloodWait as e:
        await asyncio.sleep(e.x + 1)
        await copy_message(message, chat_id)
