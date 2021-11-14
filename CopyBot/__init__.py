import os
import logging
import pyrogram
from decouple import config


# vars
APP_ID = config("APP_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
CHANNEL = config("CHANNEL", default=None)
GROUP = config("GROUP", default=None)
TO_CHANNEL = config("TO_CHANNEL", default=None)
TO_GROUP = config("TO_GROUP", default=None)
SESSION = config("SESSION", default=None)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING
)
LOGGER = logging.getLogger(__name__)
