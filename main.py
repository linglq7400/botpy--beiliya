# -*- coding: utf-8 -*-
import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import GroupMessage, Message
import MessageHandle

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()

class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_group_at_message_create(self, message: GroupMessage):
        await mh.handle_message(message) 
        
        

if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_messages=True

    # 通过kwargs，设置需要监听的事件通道
    try:
        mh = MessageHandle.MessageHandle()
        intents = botpy.Intents(public_messages=True)
        client = MyClient(intents=intents)
        client.run(appid=test_config["appid"], secret=test_config["secret"])
    except Exception as e:
        print("[ERROR] ",e)