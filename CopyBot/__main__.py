import pyrogram
from pyrogram import Client
from PyroBot import APP_ID, API_HASH, SESSION


if __name__ == "__main__":
    print("Starting Bot...")
    plugins = dict(root="PyroBot/plugins")
    app = Client(
        SESSION,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()
