#!/usr/bin/env python3

import asyncio
import logging
import os
import sys

import pykeybasebot.types.chat1 as chat1
from pykeybasebot import Bot

logging.basicConfig(level=logging.DEBUG)

if "win32" in sys.platform:
    # Windows specific event-loop policy
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


class Handler:
    async def __call__(self, bot, event):
        channel = event.msg.channel
        if event.msg.content.type_name == chat1.MessageTypeStrings.TEXT.value:
            bot.chat.send(channel, "Could you send your medical data into the chat?")
        if event.msg.content.type_name == chat1.MessageTypeStrings.ATTACHMENT.value:
            print("conversation: {} messageId: {} filename: {}".format(channel.name, event.msg.id, event.msg.content))
            filename = event.msg.content.attachment.object.filename
            os.system("keybase chat download {channel} {attachmentId} -o {filename}".format(channel = channel.name, attachmentId = int(event.msg.id), filename = filename))
            os.system("keybase fs mv {filename} /keybase/private/{doc},{patientName}".format(filename = filename, doc = bot.username, patientName = {channel.name.replace(bot.username + ",", "")}))
            os.system("keybase fs rm -f {filename}".format(filename = filename))

listen_options = {
    "filter-channels": [
        {"name": "dhrumilp15,sigilwen"}
    ]
}

bot = Bot(
    username="dhrumilp15", paperkey="holiday maid indoor dial sword leisure limit spend connect cheese round slot hat", handler=Handler()
)

asyncio.run(bot.start(listen_options))