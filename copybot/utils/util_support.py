import math
import time

# import psycopg2
from copybot import ADMINS  # , SQL_DB_URL


def is_admin(user_id):
    return user_id in ADMINS


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000

        elapsed_time = time_formatter(milliseconds=elapsed_time)
        remaining_time = time_formatter(milliseconds=time_to_completion)

        progress = "[{0}{1}] \n**Progress**: `{2}%`\n".format(
            "".join(["●" for i in range(math.floor(percentage / 5))]),
            "".join(["○" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = (
            progress
            + "`{0} of {1}`\n**Speed**: `{2}/s`\n**Remaining Time**: `{3}`\n".format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed),
                remaining_time if remaining_time != "" else "0 s",
            )
        )
        try:
            await message.edit(text="{}\n {}".format(ud_type, tmp))
        except Exception:
            pass


def humanbytes(size):
    power = 2**10
    n = 0
    power_labels = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {power_labels[n]}B"


def time_formatter(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"


# def get_db_size():
#     if not SQL_DB_URL:  # noqa: F821
#         return "Mongo DB"
#     conn = psycopg2.connect(SQL_DB_URL)  # noqa: F821
#     cursor = conn.cursor()
#     query = "SELECT pg_database_size(current_database()) / (1024.0 * 1024.0)::numeric;"
#     cursor.execute(query)
#     database_size_mb = cursor.fetchone()[0]
#     database_size_mb = float(database_size_mb) if database_size_mb is not None else 0.0
#     db_size = round(database_size_mb, 2)
#     db_size = f"SQL DB: {db_size} MB"
#     cursor.close()
#     conn.close()
#     return db_size
