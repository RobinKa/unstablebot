from battlenet.community.wow.characters import Character
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

	print("Data:", data)

	infos = []

	realm = data["realm"]
	name = data["name"]
	cl = CLASSES[int(data["class"])]
	race = RACES[int(data["race"])]

	info = "**Character** *Realm*: `%s` *Name*: `%s` *Class*: `%s` *Race*: `%s`" % (realm, name, cl, race)
	infos.append(info)

	def humanize_string(s):
		return re.sub("([a-z])([A-Z])","\g<1> \g<2>", s).title()

	for field in fields:
		info = "**%s**" % field.title()
		for k, v in data[field].items():
			if not (isinstance(v, list) or isinstance(v, dict)):
				info += " *%s*: `%s`" % (humanize_string(str(k)), humanize_string(str(v)))
		infos.append(info)

	return infos
