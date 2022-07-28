import asyncio
import random
from datetime import datetime

import discord
from discord.ext import commands, tasks

from chattattack.cat import Cat, GenerateCat
from chattattack.new_cat import new_cat
from chattattack.fishes import get_fishes
from utils.paginator import PaginatorBuilder, PaginatorController
from utils.database import DBManager
from constants import *


def embed_fail_account():
    return discord.Embed(
        title = "😨 Vous n'avez pas encore créé de compte!", 
        description = f"Pour créer un compte, écrivez dans le serveur **{PREFIX}register**", 
        color = discord.Color.red(), 
    )
    
def norm(dt):
    # * Correct some datetime conversion issues
    return TIMEZONE.normalize(dt)


class ConvertUser(commands.UserConverter):
    async def convert(self, ctx, arg):
        user = await super().convert(ctx, arg)
        return user

class CatDrops(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.user_try = {}
        self.drop.start() # * Initialiser pour chaques guilde

    def __remaining_time(self, cat, user):        
        return int(60*cat.temp['rarity'] - (datetime.now(TIMEZONE).timestamp() - self.user_try.get(user.id, 0)))

    def embed_mp(self, cat, user, success = 1):
        embed = discord.Embed(title = "🐱 Tentative de capture", 
                            description = f"x{cat.temp['rarity']} 🐟 dépensé(s)!", 
                            color = discord.Color.random())
        embed.set_thumbnail(url = cat.image)
        embed.add_field(name = "🏷 Résultat:", value = "😻 Chat attrapé!" if success else "🙀 Chat méfiant...")
        if not success:
            embed.add_field(name = "🔭 Prochain essai:", 
                            value = f"{self.__remaining_time(cat, user)} seconde(s)..." )
        return embed

    def embed_mp_sus(self, cat, user):
        embed = discord.Embed(title = "😾 Chat encore méfiant", 
                            description = f"Le chat ne vous fait pour l'instant pas confiance...", 
                            color = discord.Color.random())
        embed.set_thumbnail(url = cat.image)
        embed.add_field(name = "🔎 Prochain essai:", 
                            value = f"{self.__remaining_time(cat, user)} seconde(s)..." )
        return embed
    
    def embed_mp_nofish(self, cat, user):
        embed = discord.Embed(title = "🎣 Aucun poisson", 
                            description = f"Pour tenter de capturer ce chat, vous devez avoir des poissons.", 
                            color = discord.Color.random())
        embed.set_thumbnail(url = cat.image)
        embed.add_field(name = "🔎 Prochain essai:", 
                            value = f"{self.__remaining_time(cat, user)} seconde(s)..." )
        return embed
    
    async def _user_fish_choice(self, user, fish, cat):
        fish_info = get_fishes()
        number = cat.temp['rarity']
        fish_user = [list(map(lambda x: int(x), i.split("/"))) for i in fish.split("|") if i]
        available_fish = [i for i in fish_user if i and i[0] >= number]
        
        if not available_fish:
            return
        
        paginator = PaginatorController(self.client, user, channel=user)
        paginator.builder = PaginatorBuilder()
        paginator.builder.base_embed_create(f"🎣 Choix de poisson",
                                  f"❓ Plus un poisson est de haute qualité, plus vous aurez de chance de capturer le chat.\n😾 Plus un chat est rare, plus vous aurez besoin de poisson afin de le capturer.",
                                  discord.Colour.gold())
        paginator.builder.prefix = [fish_info[i[1]-1][1].EMOTE for i in available_fish]
        paginator.builder.content = [f"{number}/{i[0]} {fish_info[i[1]-1][0]} ➨ {min(round(cat.catch_probability * fish_info[i[1]-1][1].MODIFICATION, 2), 100)} %" for i in available_fish]
        paginator.builder.content_builder(decorator=" ➨ ")
        paginator.builder.paginator_store()
        
        result = await paginator.paginator_emote()
        await paginator.message.delete()
        if not result: return
        
        fish_id = available_fish[paginator.index][1]
        
        DBManager().user_add_fish(user.id, f"-{number}/{fish_id}")
        return min(cat.catch_probability * fish_info[fish_id-1][1].MODIFICATION, 100)
    
    async def _deep_user_checking(self, user, reaction, message, cat):        
        if user.bot or reaction.message.id != message.id or str(reaction.emoji) not in DROP_EMOJI:
            return
        
        await reaction.remove(user)
        
        if not DBManager().check_if_user_exists(user.id): # ? User dont have existing account
            await user.send(embed = embed_fail_account())
            return

        elif (datetime.now(TIMEZONE).timestamp() - self.user_try.get(user.id, 0)) < 60*cat.temp['rarity']: # ? User had try to catch cat too quickly
            await user.send(embed = self.embed_mp_sus(cat, user))
            return
        
        fish = DBManager().user_get_fish(user.id)
        probability = await self._user_fish_choice(user, fish, cat)
        
        if not probability:
            await user.send(embed = self.embed_mp_nofish(cat, user))
            return

        if random.randint(0, 100) <= probability: # ? User suceed to catch the cat
            await user.send(embed = self.embed_mp(cat, user, success = 1))
            await self._drop_success(message, user, cat)
        
        else: # ? User failed to catch the cat, add to fail dict
            self.user_try[user.id] = datetime.now(TIMEZONE).timestamp()
            await user.send(embed = self.embed_mp(cat, user, success = 0))
    

    @tasks.loop(minutes = 20.0)
    async def drop(self):
        
        def check(reaction, user: ConvertUser):
            result = asyncio.ensure_future(self._deep_user_checking(user, reaction, message, cat))
        
        channel = await self.client.fetch_channel(DROP_CHANNEL)
        cat = GenerateCat()
        await cat.grab_randomcat()
  
        message = await channel.send(embed = cat.random_embed)

        for r in DROP_EMOJI:
            await message.add_reaction(r)

        try:
            react, user = await self.client.wait_for('reaction_add', timeout = 600.0, 
                                                     check = check)  
        except asyncio.TimeoutError:
            try:
                await message.clear_reactions()
                await message.edit(content = f"🧹 Le chat c'est enfui...", delete_after = 20)
                return
            except discord.NotFound:
                pass
        
    async def _drop_success(self, message, user, cat):
        await message.clear_reactions()
        await message.edit(content = f"🎀 <@{user.id}> a réussi à capturer le chat!", delete_after = 20)
        new_cat(cat, user)
        self.user_try = {} # ! Reset the class instance user_try dict


    @drop.before_loop
    async def before_printer(self):
        await asyncio.sleep(1200)



def setup(client):
    client.add_cog(CatDrops(client))
