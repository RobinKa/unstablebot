import discord as dc
from settings import *
import bnet
import asyncio

class UnstableClient(dc.Client):
    def __init__(self):
        super().__init__()
        self.loop.create_task(self.check_guild_feed())
        self.loop.create_task(self.check_realm_status())

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

        last_check_time = None
        print("Start check news time:", last_check_time)

        channel = dc.Object(id=BOT_NEWS_CHECK_CHANNEL)

        while not self.is_closed:
            print("Checking news", last_check_time)
            success, new_guild_news, new_last_check_time = bnet.get_guild_news(since_time=last_check_time, name=BOT_NEWS_CHECK_GUILD, realm=BOT_NEWS_CHECK_REALM)
            print("Got news", success, new_last_check_time, new_guild_news)

            if success:
                guild_news, last_check_time = new_guild_news, new_last_check_time

                for news in guild_news:
                    await self.send_message(channel, news)

            await asyncio.sleep(30)

    async def check_realm_status(self):
        await self.wait_until_ready()

        realm_status = None
        realm_queue = None
        realm_population = None

        channel = dc.Object(id=BOT_REALM_STATUS_CHANNEL)

        while not self.is_closed:
            print("Checking realm status")
            success, new_realm_status, new_realm_queue, new_realm_population = bnet.get_realm_status(realm=BOT_REALM_STATUS_REALM)

            print("Got realm status", success, new_realm_status, new_realm_queue, new_realm_population)
            
            if success:
                if realm_status != None:
                    if realm_status != new_realm_status:
                        await self.send_message(channel, "%s is now %s" % (BOT_REALM_STATUS_REALM, "up" if new_realm_status else "down"))

                    if realm_queue != new_realm_queue:
                        await self.send_message(channel, "%s is %s" % (BOT_REALM_STATUS_REALM, "now in queue mode" if new_realm_queue else "not in queue mode anymore"))

                    #if realm_population != new_realm_population:
                    #    await self.send_message(channel, "%s population changed from %s to %s" % (BOT_REALM_STATUS_REALM, realm_population.title(), new_realm_population.title()))

                realm_status, realm_queue, realm_population = new_realm_status, new_realm_queue, new_realm_population

            await asyncio.sleep(30)



client = UnstableClient()
client.run(DISCORD_TOKEN)
