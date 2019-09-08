# from flask import redirect, render_template, request, session
import pykeybasebot
import asyncio
import functools
import logging
import os
import sys
import pykeybasebot.types.chat1 as chat1

logging.basicConfig(level = logging.DEBUG)

asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def force_async(fn):
    from concurrent.futures import ThreadPoolExecutor
    import asyncio

    pool = ThreadPoolExecutor()

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        future = pool.submit(fn, *args, **kwargs)
        return asyncio.wrap_future(future)

    return wrapper

# class Handler:
#     async def __call__(self, bot, event):
#         if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
#             return
#         await docbot.sharepatientdata(event.msg.content.text.body)
        
class DocBot:
    def __init__(self, botname, paperkey, channels):
        self.botname = botname
        self.paperkey = paperkey
        self.channels = channels
        self._commands = []
        self._bot = None
        self.hcp = 'dhrumilp15'

    def run(self):
        self._bot = pykeybasebot.Bot(
            username=self.botname, paperkey=self.paperkey, handler=self.command_handler
        )
        # bot_channels = []
        # for channel in self.channels:
        #     team, topic = channel.split("#")
        #     bot_channels.append(
        #         {"name": team, "topic_name": topic, "members_type": "team"}
        #     )
        listen_options = {"filter-channels": "dhrumilp15,sigilwen"}
        asyncio.run(self._bot.start(listen_options))

    def add_command(self, trigger_func, command_func):
        async_command = force_async(command_func)
        self._commands.append(
            {"trigger_func": trigger_func, "command_func": async_command}
        )

    def reply(self, event, message):
        channel = event.msg.channel  # format the channel for sending
        # make a new loop to run the async bot.chat.send method in what is currently
        # a synchronous context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._bot.chat.send(channel, message))

    async def command_handler(self, bot, event):
        for possibility in self._commands:
            if possibility["trigger_func"](self, event):
                return await possibility["command_func"](self, event)
    
    async def sharepatientdata(self, patient):
        # Technically don't need to force because folder should be empty but just in case
        os.system("keybase fs cp -r -f /keybase/private/{patient} /keybase/private/{patient},{hcp}".format(patient = patient, hcp = self.hcp))
    
    async def updatepatientsdata(self,patient):
        os.system("keybase fs cp -r -f /keybase/private/{hcp} /keybase/private/{hcp},{patient}".format(hcp = self.hcp, patient = patient))
    
    async def deletepatientdata(self):
        os.system("keybase fs rm -r -f /keybase/private/{hcp}".format(hcp = self.hcp))

docbot = DocBot(
    botname = "dhrumilp15",
    paperkey = "seek ethics twelve federal garment hockey vapor local vacuum bleak employ egg soap",
    channels = ["dhrumilp15,sigilwen"]
)
def patientGreeting(bot, event):
    if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
        return False
    return event.msg.content.text.body == "I'm at the doctor's"

def askHistory(bot, event):
    if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
        return False
    bot.reply(event, "Could you please send your medical history in the chat.")

docbot.add_command(patientGreeting, askHistory)

def gethistory(bot, event):
    if event.msg.content.type_name

docbot.run()