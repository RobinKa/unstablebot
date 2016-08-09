import discord as dc
from settings import *
import bnet

class UnstableClient(dc.Client):
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

client = UnstableClient()
client.run(DISCORD_TOKEN)
