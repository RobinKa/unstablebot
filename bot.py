import discord as dc
from settings import *
import bnet
import asyncio
import datetime

class UnstableClient(dc.Client):
    def __init__(self):
        super().__init__()
        self.loop.create_task(self.check_guild_feed())

    async def on_ready(self):
        print("Ready")
        print("Name:", self.user.name)
        print("Id:", self.user.id)
        print("------")

    async def on_message(self, message):
        message_split = message.content.split(maxsplit=1)
        if len(message_split) == 2:
            message_start, message_rest = message_split[0].lower(), message_split[1]

            if message_start.startswith(BOT_TRIGGER):
                await self.on_command(message.channel, message_start[len(BOT_TRIGGER):], message_rest)

    async def on_command(self, channel, command, payload):
        try:
            payload_split = payload.split()
            print("Payload split:", payload_split)

            if command == "info":
                char_name, realm = UnstableClient._get_name_realm(payload_split[0])
                fields = payload_split[1:]
                infos = bnet.get_info(char_name, realm, fields)
                
                for info in infos:
                    print(info)
                    await self.send_message(channel, info)

        except Exception as ex:
            print("Exception in command handling", command, payload)
            print(ex)

    def _get_name_realm(s):
        if "@" in s:
            split = s.split("@", maxsplit=1)
            char_name = split[0]
            realm = split[1]
            return char_name, realm
        else:
            char_name = s
            return char_name, BNET_REALM

    async def check_guild_feed(self):
        await self.wait_until_ready()

        last_check_time = int(datetime.datetime.utcnow().timestamp())
        print("Start check news time:", last_check_time)

        channel = dc.Object(id=BOT_NEWS_CHECK_CHANNEL)

        while not self.is_closed:
            print("Checking news", last_check_time)
            guild_news, last_check_time = bnet.get_guild_news(since_time=last_check_time, name=BOT_NEWS_CHECK_GUILD, realm=BOT_NEWS_CHECK_REALM)
            print("Got news", last_check_time, guild_news)
            for news in guild_news:
                await self.send_message(channel, news)

            await asyncio.sleep(30)

client = UnstableClient()
client.run(DISCORD_TOKEN)
