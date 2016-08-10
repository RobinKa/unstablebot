from battlenet.community.wow.characters import Character
from battlenet.community.wow.guilds import Guild
from battlenet.community.wow.realms import Realm
from battlenet.oauth2 import BattleNetOAuth2
from settings import *
import re

RACES = {
    1: "Human",
    2: "Orc",
    3: "Dwarf",
    4: "Night Elf",
    5: "Undead",
    6: "Tauren",
    7: "Gnome",
    8: "Troll",
    9: "Goblin",
    10: "Blood Elf",
    11: "Draenei",
    22: "Worgen",
    24: "Pandaren (N)",
    25: "Pandaren (H)",
    26: "Pandaren (A)",
}

CLASSES = {
    1: "Warrior",
    2: "Paladin",
    3: "Hunter",
    4: "Rogue",
    5: "Priest",
    6: "Death Knight",
    7: "Shaman",
    8: "Mage",
    9: "Warlock",
    10: "Monk",
    11: "Druid",
    12: "Demon Hunter",
}

def get_info(name, realm=BNET_REALM, fields=[]):
    print("Fields:", fields)

    char = Character(apikey=BNET_KEY, realm=realm, name=name, fields=fields)
    status_code, data = char.get()

    print("Status code:", status_code)
    print("Data:", data)

    infos = []

    realm = data["realm"]
    name = data["name"]
    cl = CLASSES[int(data["class"])]
    race = RACES[int(data["race"])]

    info = "**Character** Realm: `%s` Name: `%s` Class: `%s` Race: `%s`" % (realm, name, cl, race)
    infos.append(info)

    def humanize_string(s):
        return re.sub("([a-z])([A-Z])","\g<1> \g<2>", s).title()

    for field in fields:
        info = "**%s**" % field.title()
        for k, v in data[field].items():
            if not (isinstance(v, list) or isinstance(v, dict)):
                info += " %s: `%s`" % (humanize_string(str(k)), humanize_string(str(v)))
        infos.append(info)

    return infos

def get_guild_news(since_time, name, realm=BNET_REALM):
    guild = Guild(apikey=BNET_KEY, name=name, realm=realm, fields=["news"])
    status_code, data = guild.get()

    print("GetGuildNews", since_time, "status:", status_code)

    if status_code != 200:
        return False, None, None

    news = []
    newest_time = since_time if since_time is not None else 0

    for n in data["news"]:
        news_time = int(n["timestamp"]) // 1000

        if since_time is not None and news_time > since_time:
            news_type = n["type"]

            if news_type == "playerAchievement":
                news.append("*`%s` gained achievement `%s`*" % (n["character"], n["achievement"]["title"]))

        if news_time > newest_time:
            newest_time = news_time

    return True, news, newest_time

def get_realm_status(realm=BNET_REALM):
    realms = Realm(apikey=BNET_KEY, realms=[realm])
    status_code, data = realms.get()
    
    print("Realm status received:", status_code, data)

    if status_code != 200:
        return False, None, None, None

    realm_status = data["realms"][0]["status"]
    realm_queue = data["realms"][0]["queue"]
    realm_population = data["realms"][0]["population"]

    return True, realm_status, realm_queue, realm_population
