#!/usr/bin/env python3

import asyncio
import logging
import os
import sys

import pykeybasebot.types.chat1 as chat1
from pykeybasebot import Bot

class DocBot:
    def __init__(self, botname, paperkey):
        self.botname =botname
        self.paperkey =paperkey
        self._bot = None
    logging.basicConfig(level=logging.DEBUG)

    if "win32" in sys.platform:
        # Windows specific event-loop policy
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
 
    listen_options = {
        "filter-channels": [
            {"name": "dhrumilp15,someoneelse"}
        ]
    }

    bot = Bot(
        username = "dhrumilp15", paperkey = "holiday maid indoor dial sword leisure limit spend connect cheese round slot hat", handler = Handler
    )
    asyncio.run(bot.start(listen_options))

class Handler:
    async def __call__(self, bot, event):
        channel = event.msg.channel
        patient = channel.name.replace(bot.username + ",", "")
        doctor = bot.username
        if event.msg.content.text.body == "I'm at the doctor's":
            await bot.chat.send(channel, "Could you send your medical data into the chat?")
        if event.msg.content.text.body == "Your updated files have been added to your shared folder and you should copy them into your private folder." and event.msg.sender.username == bot.username:
            os.system("keybase fs cp -r -f /keybase/private/{}, /keybase/private/{},{}".format(doctor, doctor, patient))

        if event.msg.content.type_name == chat1.MessageTypeStrings.ATTACHMENT.value:
            print("conversation: {} messageId: {} filename: {}".format(channel.name, event.msg.id, event.msg.content))
            filename = event.msg.content.attachment.object.filename
            os.system("keybase chat download {channel} {attachmentId} -o {filename}".format(channel = channel.name, attachmentId = int(event.msg.id), filename = filename))
            os.system("keybase fs mv {filename} /keybase/private/{doc},{patientName}".format(filename = filename, doc = bot.username, patientName = patient))
            os.system("keybase fs rm -f {filename}".format(filename = filename))
