

import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import errors
from helpers.filters import command


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"])
    & ~filters.private
    & ~filters.bot
)
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>__promote me as admin first__ !</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Sayuvc"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(
            message.chat.id, "__i'm joined here for playing music on voice chat__"
        )
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>__Sayuvc already joined group.</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 Flood Wait Error 🛑 \n\n User {user.first_name} couldn't join your group due to heavy join requests for userbot."
            "\n\nor manually add assistant to your Group and try again</b>",
        )
        return
    await message.reply_text(
        f"<b>Yeah __SayuVc Here__.</b>",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"])
    & filters.group
    & ~filters.edited
)
async def rem(client, message):
    try:
        await USER.send_message(message.chat.id, "__Sayuvc left  the group__")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>user couldn't leave your group, may be floodwaits.\n\nor manually kick me from your group</b>"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
async def bye(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("Assistant Leaving all chats")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Assistant leaving all group... \n\nLeft: {left} chats. Failed: {failed} chats."
            )
        except:
            failed += 1
            await lol.edit(
                f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"Left {left} chats. Failed {failed} chats."
    )


