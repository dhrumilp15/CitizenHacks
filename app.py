import re
from flask import Flask, abort, redirect, render_template, request
from werkzeug.exceptions import default_exceptions, HTTPException

import pykeybasebot
import asyncio
import functools
import logging
import os
import sys
import pykeybasebot.types.chat1 as chat1
# Web app
app = Flask(__name__)

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

logging.basicConfig(level = logging.ERROR)

if 'win32' in sys.platform:
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
        bot_channels = []
        for channel in self.channels:
            team, topic = channel.split("#")
            bot_channels.append(
                {"name": team, "topic_name": topic, "members_type": "team"}
            )
        listen_options = {"filter-channels": bot_channels}
        asyncio.run(self._bot.start(listen_options))

    def add_command(self, trigger_func, command_func):
        async_command = force_async(command_func)
        self._commands.append(
            {"trigger_func": trigger_func, "command_func": async_command}
        )

    def reply(self, event, message):
        channel = event.msg.channel.replyable_dict()  # format the channel for sending
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
    paperkey = "holiday maid indoor dial sword leisure limit spend connect cheese round slot hat",
    channels = ["dhrumilp15,dhrumilp15"]
)

# await docbot._bot.chat.send(...)
def patientres(basicbot, event):
    if event.msg.content.type_name != chat1.MessageTypeStrings.TEXT.value:
        return False
    return [event.msg.sender.username, event.msg.text.body]

@app.route("/medhistory", methods = ['GET', 'POST'])
def names():
    if request.method == 'GET':
        return render_template("names.html")
    else:
        await docbot.sharepatientdata()