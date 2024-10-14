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
from contextlib import asynccontextmanager

import aiosqlite

from copybot import LOGGER


# Async context manager for database connection
@asynccontextmanager
async def get_db_connection():
    conn = await aiosqlite.connect("chats.db")  # Use aiosqlite to connect
    try:
        yield conn  # Yield the connection instead of the cursor
        await conn.commit()  # Commit changes asynchronously
    finally:
        await conn.close()  # Close the connection asynchronously


# Async function to initialize the database (create table if not exists)
async def init_db():
    async with get_db_connection() as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_channel INTEGER NOT NULL,
                destination_channel INTEGER NOT NULL
            )
            """
        )


# Async function to add a mapping to the database
async def add_chats(source, destination):
    async with get_db_connection() as db:
        existing_chat = await db.execute(
            "SELECT 1 FROM chats WHERE source_channel = ? AND destination_channel = ?",
            (source, destination),
        )
        if await existing_chat.fetchone() is not None:
            print("Duplicate entry found, skipping addition.")
            return "exists"
        await db.execute(
            "INSERT INTO chats (source_channel, destination_channel) VALUES (?, ?)",
            (source, destination),
        )
        LOGGER.info(f"Added chat from {source} to {destination}")
        return True


async def remove_chats(source, destination):
    async with get_db_connection() as db:
        existing_chat = await db.execute(
            "SELECT 1 FROM chats WHERE source_channel = ? AND destination_channel = ?",
            (source, destination),
        )
        if await existing_chat.fetchone() is None:
            print("No chat found to remove.")
            return "not found"
        await db.execute(
            "DELETE FROM chats WHERE source_channel = ? AND destination_channel = ?",
            (source, destination),
        )
        LOGGER.info(f"Removed chat from {source} to {destination}")
        return True


# Async function to get all destination channels for a given source channel
async def get_chats(source):
    async with get_db_connection() as db:
        async with db.execute(
            "SELECT destination_channel FROM chats WHERE source_channel = ?", (source,)
        ) as cursor:
            return [int(row[0]) for row in await cursor.fetchall()]


# Async function to get all chats (source and destination channels)
async def get_all_chats():
    async with get_db_connection() as db:
        async with db.execute(
            "SELECT source_channel, destination_channel FROM chats"
        ) as cursor:
            return await cursor.fetchall()


async def get_source_channels():
    async with get_db_connection() as db:
        async with db.execute("SELECT source_channel FROM chats") as cursor:
            source_channels = await cursor.fetchall()
            return [int(row[0]) for row in source_channels]


async def get_dest_by_source(source):
    async with get_db_connection() as db:
        async with db.execute(
            "SELECT destination_channel FROM chats WHERE source_channel = ?",
            (source,),
        ) as cursor:
            destination_channels = await cursor.fetchall()
            return [int(row[0]) for row in destination_channels]


# Initialize the database when this module is imported
def init_database():
    # Check if there's an existing event loop
    try:
        asyncio.get_running_loop()
        # If there is, create a task instead of running it directly
        asyncio.create_task(init_db())
    except RuntimeError:
        # If there's no event loop running, we can safely run it
        asyncio.run(init_db())


init_database()
