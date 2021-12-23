import pyrogram
from pyrogram import Client
from CopyBot import APP_ID, API_HASH, SESSION


if __name__ == "__main__":
    print("Starting Bot...")
    plugins = dict(root="CopyBot/plugins")
    app = Client(
        SESSION,
        api_id=APP_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()
