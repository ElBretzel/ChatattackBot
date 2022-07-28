import random
import os
import json

from utils.database import DBManager
from constants import RESSOURCES_DIRECTORY

with open(os.path.join(RESSOURCES_DIRECTORY, "catname.json"), "r") as f:
    NAME = json.load(f)

def __reformat_list_db(liste):
    return f"{'|'.join([str(i) for i in liste])}"

def new_cat(cat, user):

    cat_name = random.choice(NAME)

    DBManager().add_cat(user.id, cat_name, level = cat.stats["level"], 
            furtivity = __reformat_list_db(cat.stats["furtivity"]), 
            intelligence = __reformat_list_db(cat.stats["intelligence"]), 
            aggressivity = __reformat_list_db(cat.stats["aggressivity"]), 
            health = __reformat_list_db(cat.stats["health"]), 
            rarity = cat.temp["rarity"], 
            hiden_bonus = cat.temp["hiden_bonus"], 
            affection = f"{cat.temp['affection']}|100", 
            energy = f"{cat.temp['energy']}|100", 
            hygien = f"{cat.temp['hygien']}|100", 
            sleep = f"{cat.temp['sleep']}|100", 
            hunger = f"{cat.temp['hunger']}|100", 
            wiki = cat.wiki, 
            image = cat.image)

    DBManager().set_cat_weapon(user.id)