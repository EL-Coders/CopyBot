import logging
import logging.config
import os
import re

from dotenv import load_dotenv

load_dotenv(override=True)

pattern = re.compile(r"^.\d+$")

# vars
APP_ID = int(os.environ.get("APP_ID", default=None))
API_HASH = os.environ.get("API_HASH", default=None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", default=None)
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
SESSION = os.environ.get("SESSION", "")
ADMINS = [
    int(user) if pattern.search(user) else user
    for user in os.environ.get("ADMINS", "").split()
] + [OWNER_ID]


# logging Conf
logging.config.fileConfig(fname="config.ini", disable_existing_loggers=False)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
