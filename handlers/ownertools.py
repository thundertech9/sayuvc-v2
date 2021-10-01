
import os
import shutil
import sys
import traceback
from os import environ, execle

import psutil
from helpers.filters import command
from pyrogram import Client, filters
from handlers.songs import get_text, humanbytes
from pyrogram.types import Message
from helpers.database import db


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
        text=f"****System Stats**** \n\n** »__bot version__** `v2.0` \n\n** »__total users__** \n » **__on bot pm__** `{total_users}` \n\n** »__disk usage__** \n » ** »__disk space__** `{total}` \n » **__used__** `{used}({disk_usage}%)` \n » **__free__** `{free}` \n\n****hardware usage**** \n » **>CPU usage:** `{cpu_usage}%` \n > **RAM usage:** `{ram_usage}%`",
        parse_mode="Markdown",
        quote=True,
    )
