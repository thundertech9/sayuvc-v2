#This Code Owned By @Itz_Samrat


import os
import shutil
import sys
import traceback
from time import time
from datetime import datetime
from os import environ, execle



import psutil
from helpers.database import db
from pyrogram.types import Message
from helpers.filters import command
from pyrogram import Client, filters
from config import BOT_NAME, BOT_USERNAME
from handlers.songs import get_text, humanbytes

START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)

# Stats Of Your Bot
@Client.on_message(command("sysinfo"))
async def botstats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    total = humanbytes(total)
    used = humanbytes(used)
    free = humanbytes(free)
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent
    total_users = await db.total_users_count()
    await message.reply_text(
        text=f"** **System Stats of Sayu** ** \n\n** ❂__bot version__** `v2.0` \n\n** __M-Stats__ {total_users} __Users__ \n\n** **Disk Usage** ** \n » **__disk space__** `{total}` \n » **__used__** `{used}({disk_usage}%)` \n » **__free__** `{free}` \n\n** **hardware usage** ** \n > **CPU** __usage__: `{cpu_usage}%` \n > **RAM** __Usage__: `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True,
    )

@Client.on_message(command(["mping", f"mping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `PONG!!`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")

@Client.on_message(command(["uptime", f"mstart"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "MUSIC Bot Is Running:\n"
        f"• **__Ping__:** `error ms`\n"
        f"• **__Uptime__:** `{uptime}`\n"
        f"• **__Start time__:** `{START_TIME_ISO}`"
    )
