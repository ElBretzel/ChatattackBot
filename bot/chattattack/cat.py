import random
import os
from datetime import datetime, timedelta
import asyncio
import math
from enum import Enum

from PIL import Image
import numpy as np
import discord
import scipy.stats

from chattattack.api_grabber import cat_request
from constants import *
from utils.database import DBManager
from utils.change_utc import convert_timezone

with open(os.path.join(KEY_DIRECTORY, "catapi-key.txt"), "r") as f:
    KEY = f.read()    
    
def _reformat_calc(stats):
    splitted_stats = stats.split("|")
    base, effort = splitted_stats[0], splitted_stats[1]
    return base, effort

def norm(dt):
    # * Correct some datetime conversion issues
    return TIMEZONE.normalize(dt)

class CatRarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5
    COSMIC = 6

class Cat:
    def __init__(self, name, temp, stats, wiki, image, last_care, cat_id, owner_id):
        self.name = name
        self.temp = temp
        self.stats = stats
        self.wiki = wiki
        self.image = image
        self.last_care = convert_timezone(datetime.strptime(last_care, r"%Y-%m-%d %H:%M:%S"))
        self.cat_id = cat_id
        self.owner_id = owner_id
        self.update_stats()

    def calc_stats(self, base, effort = 0, hiden = 0):
        return math.floor((((float(base) + float(hiden)) * 2 + math.floor(math.floor(math.sqrt(int(effort)))/4)) * self.stats['level']) / 100) + 5
    
    def calc_hp(self, base, effort = 0, hiden = 0):
        return math.floor((((float(base) + float(hiden)) * 2 + math.floor(math.floor(math.sqrt(float(effort)))/4)) * self.stats['level']) / 100) + self.stats['level'] + 10
    
    def update_stats(self):

        def stat_level(name):
            return int(self.temp[name].split("|")[0])
        
        def stat_status(name):
            return int(self.temp[name].split("|")[1])

        def diff_time():
            return (datetime.now(TIMEZONE).timestamp() - self.last_care.timestamp())//3600
        
        def update(name, cap = 1):
            # * Return the formula which update stats over time
            return math.floor( ( ( -8+1.35** stat_level(name) ) *diff_time() ) // cap)
        
        if diff_time():
            self.temp["affection"] = f"{stat_level('affection')}|{max(stat_status('affection') + update('affection', 6), 0)}"
            self.temp["energy"] = f"{stat_level('energy')}|{max(stat_status('energy') + update('energy', 4), 0)}"
            self.temp["hygien"] = f"{stat_level('hygien')}|{max(stat_status('hygien') + update('hygien', 2), 0)}"
            self.temp["sleep"] = f"{stat_level('sleep')}|{max(stat_status('sleep') + update('sleep', 3), 0)}"
            self.temp["hunger"] = f"{stat_level('hunger')}|{max(stat_status('hunger') + update('hunger', 5), 0)}"
            self.last_care = norm(datetime.now(TIMEZONE) - timedelta(hours = diff_time()))
            
            DBManager().update_cat_stat(self.cat_id, self.last_care, **self.temp)
        
    @property
    def info_cat_embed(self):
        
        main_id = DBManager().user_get_maincat(self.owner_id)
        desc_message = f"👊 **{self.name}** est votre compagnon principal." if main_id and main_id[0] == self.cat_id else\
                       f"📌 Pour s'occuper de **{self.name}**, faites **{PREFIX}main {self.cat_id}**."
        
        embed = discord.Embed(title = f"😸 Statistiques de {self.name}", 
                              description = desc_message, 
                              colour = discord.Colour.random())
        embed.set_thumbnail(url = self.image)
        
        hiden = self.temp['hiden_bonus']
        
        embed.add_field(name = "Niveau: ", value = self.stats['level'], inline = True)
        embed.add_field(name = "Santé: ", value = self.calc_hp(*_reformat_calc(self.stats['health']), hiden), inline = True)
        embed.add_field(name = "Race: ", value = f"[:Clique:]({self.wiki})", inline = True)
        embed.add_field(name = "Furtivité: ", value = self.calc_stats(*_reformat_calc(self.stats['furtivity']), hiden), inline = True)
        embed.add_field(name = "Intelligence: ", value = self.calc_stats(*_reformat_calc(self.stats['intelligence']), hiden), inline = True)
        embed.add_field(name = "Aggresivité: ", value = self.calc_stats(*_reformat_calc(self.stats['aggressivity']), hiden), inline = True)
        return embed
                
                
class GenerateCat(Cat):
    def __init__(self):
        self.data = None

    async def grab_randomcat(self, is_starting = 0):
        breeds = await cat_request('https://api.thecatapi.com/v1/breeds', KEY)
        breeds_id = [i["id"].lower() for i in breeds]
        random_breed = random.choice(breeds_id)
        cat_data = await cat_request(f"https://api.thecatapi.com/v1/images/search?breed_ids={random_breed}", KEY)
        self.data = cat_data
        await self.define_cat(cat_data, is_starting)
    
    def random_rarity(self, is_rare):
        if is_rare:
            probability = [2.125, 5.25, 11.5, 16.125, 20, 45]
        else:
            probability = [1.5625, 3.125, 6.25, 12.5, 25, 50]
        random_number = random.uniform(0, 98.4375)
        
        for p, i in zip(probability, range(6, 0, -1)):
            if random_number <= p:
                break
        return i    
        
    async def define_cat(self, data, is_starting):
        if not is_starting:
            rarity_id = self.random_rarity(int(data[0]["breeds"][0]["rare"]))
        else:
            rarity_id = 1
        
        stat_rarity = rarity_id // 2
        health = int(data[0]['breeds'][0]['life_span'].split("-")[1])+random.randint(-3+stat_rarity, stat_rarity)
        self.stats = {
                     "level": self.cat_level if not is_starting else 10, 
                     "furtivity": [int(data[0]["breeds"][0]["adaptability"])+random.randint(-3+stat_rarity, stat_rarity), 0], 
                     "intelligence": [int(data[0]["breeds"][0]["intelligence"])+random.randint(-3+stat_rarity, stat_rarity), 0], 
                     "aggressivity": [int(data[0]["breeds"][0]["stranger_friendly"])+random.randint(-3+stat_rarity, stat_rarity), 0], 
                     "health": [health, 0, health]}
    
        hiden_bonus = random.randint(1, 8)*math.sqrt(rarity_id)
        
        self.temp = { 
                     "rarity": rarity_id, 
                     "hiden_bonus": min(hiden_bonus, 16), 
                     "affection": int(data[0]['breeds'][0]['affection_level']), 
                     "energy": int(data[0]['breeds'][0]['energy_level']), 
                     "hygien": int(data[0]['breeds'][0]['grooming']), 
                     "sleep": random.randint(1, math.ceil(6-math.sqrt(rarity_id))), 
                     "hunger": random.randint(1, math.ceil(6-math.sqrt(rarity_id)))}
        
        self.wiki = data[0]["breeds"][0]["wikipedia_url"]
        self.image = data[0]["url"]
    
    @property
    def cat_level(self):
        clock = datetime.now(TIMEZONE)
        hour_mod = scipy.stats.norm(12, 6).cdf(abs(clock.hour-12))
        random_level = random.randint(5, 15+abs(clock.hour-12))
        normal_level = np.random.normal(random_level, 2)
        return abs(np.floor(normal_level*np.exp(hour_mod)*random.uniform(0.95, 1.05))) or 1.0
    
    @property
    def catch_probability(self):
        return int((1/(0.2+1.4**self.temp['rarity']))*100)
    
    @property
    def random_embed(self):
        embed = discord.Embed(
            title = f"🐈 Un chat est apparu (**{CatRarity(self.temp['rarity']).name}**)!", 
            description = f"⏰ Vous avez 5 minutes pour être le premier à récupérer ce chat.\n 🔗 Chance de capture : {self.catch_probability}%", 
            colour = discord.Colour.random())
        embed.set_image(url = self.image)
        
        hiden = self.temp['hiden_bonus']
        
        embed.add_field(name = "Niveau: ", value = self.stats['level'], inline = True)
        embed.add_field(name = "Santé: ", value = self.calc_hp(self.stats['health'][0], hiden), inline = True)
        embed.add_field(name = "Race: ", value = f"[:Clique:]({self.wiki})", inline = True)
        embed.add_field(name = "Furtivité: ", value = self.calc_stats(self.stats['furtivity'][0], hiden), inline = True)
        embed.add_field(name = "Intelligence: ", value = self.calc_stats(self.stats['intelligence'][0], hiden), inline = True)
        embed.add_field(name = "Aggresivité: ", value = self.calc_stats(self.stats['aggressivity'][0], hiden), inline = True)
        
        return embed

    
    
# at the end of a battle, on stat
# effort increase by (1 random base stat value)
# effort cant go higher than 512

# + c'est rare, plus tt actions ont de chance de réussir
# + c'est rare, - le level up est rapide
# + c'est rare, - de chance pour attraper

# santé V
# defense ( depend de la rarité + hygiene + sommeil)
# aggressivity (forme / exercices) V
# furtivity (vitesse) V
# intelligence V
# faim ( + c'est rare, + c'est rapide)
# recup V
# amour V
# sommeil ( + c'est rare, + c'est rapide)
# hygiene V