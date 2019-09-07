from flask import redirect, render_template, request, session
import pykeybasebot
import asyncio
import functools
import logging
import os
import sys

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

class Handler:
    async def __call__(self, bot, event):
        print(event)

class DocBot:
    def __init__(self, botname, paperkey, channels):
        self.botname = botname
        self.paperkey = paperkey
        self.channels = channels
        self._bot = None

    def run(self):
        self._bot = pykeybasebot.Bot(
            username = self.botname, paperkey = self.paperkey, handler = Handler()
        )

    def sharepatientdata(self, patient, hcp):
        # Technically don't need to force because folder should be empty but just in case
        os.system("keybase fs cp -rf /keybase/private/{patient} /keybase/private/{patient},{hcp}".format(patient,patient,hcp))
    
    def updatepatientsdata(self,patient,hcp):
        os.system("keybase fs cp -rf /keybase/private/{hcp} /keybase/private/{hcp},{patient}".format(hcp,patient,hcp))
    
    def deletepatientdata(self, hcp):
        os.system("keybase fs rm -rf /keybase/private/{hcp}".format(hcp))
    
