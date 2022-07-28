import asyncio
from datetime import datetime, timedelta
import itertools
from io import BytesIO

from discord.ext import commands, tasks
import discord

from constants import *
from chattattack.cat import Cat, GenerateCat, CatRarity
from chattattack.new_cat import new_cat
from chattattack.foods import get_foods
from chattattack.fishes import get_fishes
from chattattack.toys import get_toys
from chattattack.card import Card
from utils.database import DBManager
from utils.paginator import PaginatorBuilder, PaginatorController
from utils.checks import check_if_registered
from utils.change_utc import convert_timezone
from utils.error_handler import *


def reformat_db_cat(response):
    name = response[0]
    temp = {
        "rarity": response[6],
        "hiden_bonus": response[7],
        "affection": response[8],
        "energy": response[9],
        "hygien": response[10],
        "sleep": response[11],
        "hunger": response[12]}
    stats = {
        "level": response[1],
        "furtivity": response[2],
        "intelligence": response[3],
        "aggressivity": response[4],
        "health": response[5]}
    wiki = response[13]
    image = response[14]
    last_care = response[15]

    return name, temp, stats, wiki, image, last_care


def norm(dt):
    # * Correct some datetime conversion issues
    return TIMEZONE.normalize(dt)


class CatCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def register(self, ctx, *args):

        await ctx.message.delete()
        already_registered = DBManager().add_user(ctx.author.id)

        if not already_registered:
            embed = discord.Embed(
                title=f"😎 Compte crée!",
                description=f" <@{ctx.author.id}> vient de rejoindre l'aventure.\n**Veillez regarder vos messages privés avant de continuer.**",
                color=discord.Colour.green())

            cat = GenerateCat()
            await cat.grab_randomcat(is_starting=1)
            new_cat(cat, ctx.author)
            cat_id = DBManager().get_last_user_cat(ctx.author.id)
            DBManager().user_set_maincat(ctx.author.id, cat_id)
            embed.set_image(url=cat.image)
            embed.add_field(name=f"🐱 Premier chat obtenu !",
                            value=f"❓ Toutes les commandes sont listées dans le **{PREFIX}help**")
            delete_after = None

        else:
            embed = discord.Embed(
                title=f"😵 Compte déjà existant!",
                description=f"Ton compte existe déjà...\nPour recommencer ton aventure, écris **{PREFIX}restart**",
                color=discord.Colour.red())
            delete_after = 30

        embed.set_footer(text=f"• Requête de {ctx.author}")
        await ctx.send(embed=embed, delete_after=delete_after)

    @commands.command()
    @commands.check(check_if_registered)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cats(self, ctx):
        
        
        cats = DBManager().get_all_user_cat(ctx.author.id)
        content = [f"**{name}**: level {level}. 《**{CatRarity(rarity).name}**》" for name, level, rarity, id_ in
                  cats]

        paginator = PaginatorController(self.client, ctx.author, ctx.channel)
        paginator.builder = PaginatorBuilder()
        paginator.builder.base_embed_create(f"🏆 Chats de {ctx.author}",
                                  f"❓ Pour plus d'information sur un de vos chats, écrivez le chiffre correspondant à celui-ci.",
                                  discord.Colour.gold(),
                                  field=[["📈 Niveau:", "Ordre décroissant", True], ["💎 Rarité:", "Ordre décroissant", True], ["\u200b", "\u200b", True]])
        paginator.builder.prefix = "/number/"
        paginator.builder.content = content
        paginator.builder.content_builder(decorator=" ➨ ")
        paginator.builder.paginator_store()
        
        result = await paginator.paginator_message()
        await paginator.message.delete()
        if not result: return
        
        cat_id = cats[paginator.index][3]
                
        response = DBManager().get_info_cat(ctx.author.id, cat_id)[2:]
        cat = Cat(*reformat_db_cat(response), cat_id, ctx.author.id)

        embed = cat.info_cat_embed
        embed.set_footer(text=f"• Requête de {ctx.author}")
        await ctx.send(embed=embed)

    @commands.check(check_if_registered)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def restart(self, ctx):

        await ctx.message.delete()

        def check(reaction, user):
            return (not user.bot) and reaction.message.id == message.id and str(
                reaction.emoji) in DELETE_CANCEL and user.id == ctx.author.id

        embed = discord.Embed(title="🙀 Voulez vous vraiment supprimer votre compte",
                              description="⚠️ Vous ne pourrez plus retourner en arrière\n🗑 = **Supprimer** | ❌ = **Annuler**!",
                              colour=discord.Colour.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"• Requête de {ctx.author}")
        message = await ctx.send(embed=embed)

        for r in DELETE_CANCEL:
            await message.add_reaction(r)

        try:
            react, user = await self.client.wait_for('reaction_add', timeout=120.0,
                                                     check=check)
        except asyncio.TimeoutError:
            await message.delete()
            return
        await message.clear_reactions()

        if str(react.emoji) != DELETE_CANCEL[0]:
            await message.delete()
            return

        DBManager().delete_user(ctx.author.id)
        embed = discord.Embed(title="💔 Ton compte vient d'être supprimé",
                              description=f"🌐 Tu peux revenir dans l'aventure avec la commande **{PREFIX}register**",
                              colour=discord.Colour.red())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_footer(text=f"• Requête de {ctx.author}")
        await message.edit(embed=embed, delete_after=60)

    @commands.check(check_if_registered)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def daily(self, ctx):

        def set_daily_message(current_streak):
            current_streak = current_streak or len(DAILY_EMOTE)
            return [str(self.client.get_emoji(v[0])) if n < current_streak else str(self.client.get_emoji(v[1])) for
                    n, v in enumerate(
                    DAILY_EMOTE)]  # ? Return the list of all highlited streak emote <= current_streak then all not highlited streak emote

        def reset():
            return discord.Embed(title="🎈 Daily streak reset.",
                                 description="Tu n'as pas réclamé ta récompense quotidienne pendant plus de 2 jours.\nTon daily streak global a été remis à zéro...",
                                 colour=discord.Colour.red())

        def cooldown(streak_time, new_daily, last_daily):
            remaining_streak = (streak_time - (new_daily - last_daily)).total_seconds() // 3600
            return discord.Embed(
                title="⌚ Daily cooldown.",
                description=f"Tu as déjà réclamé ta récomense quotidienne.\nTu peux revenir réeffectuer la commande dans **{int(remaining_streak)} heure(s).**",
                colour=discord.Colour.teal(),
            )

        def success(current_streak):
            return discord.Embed(title="🤩 Nouveau palier atteint!",
                                 description=f"{''.join(set_daily_message(current_streak))}",
                                 colour=discord.Colour.green())

        def streak(global_streak, current_streak):
            completed = int((global_streak + 1) // len(DAILY_EMOTE))
            bonus_money = completed * STREAK_MONEY
            DBManager().user_add_money(ctx.author.id, bonus_money)
            return discord.Embed(
                title=f"😻 Tu viens de compléter ton {completed} streak!",
                description=f"{''.join(set_daily_message(current_streak))}\n🎁: **{bonus_money}** {str(self.client.get_emoji(EMOTE_MONEY))}",
                colour=discord.Colour.gold(),
            )

        streak_time = timedelta(days=1)
        last_daily = convert_timezone(DBManager().user_get_daily(ctx.author.id))
        new_daily = datetime.now(TIMEZONE)
        global_streak = DBManager().user_get_streak(ctx.author.id)  # * All streak
        current_streak = (global_streak + 1) % len(DAILY_EMOTE)  # * Represent the advancement of the streak

        if (new_daily - last_daily).days >= 2:  # ? Player break his streak for more than 2 days -> resetting
            DBManager().user_reset_streak(ctx.author.id)
            current_streak = global_streak = 1
            embed = reset()
            embed.set_footer(text=f"• Requête de {ctx.author}")
            await ctx.send(embed=embed)

        if not (last_daily <= norm(new_daily - streak_time)):  # ? Player use the command too quickly (less than 1 day)
            embed = cooldown(streak_time, new_daily, last_daily)

        else:  # ? Player verify all the conditions
            DBManager().user_set_daily(ctx.author.id)
            DBManager().user_add_streak(ctx.author.id, global_streak)
            DBManager().user_add_money(ctx.author.id, DAILY_MONEY)
            DBManager().user_add_fish(ctx.author.id, DAILY_FISH)
            embed = success(current_streak)

        if not current_streak and last_daily <= norm(
                new_daily - streak_time):  # ? If the streak == max_streak and player verify all previous conditions
            embed = streak(global_streak, current_streak)

        embed.set_footer(text=f"• Requête de {ctx.author}")
        await ctx.send(embed=embed)

    @commands.check(check_if_registered)
    @commands.command()
    async def main(self, ctx, cat_id: int):

        response = DBManager().get_info_cat(ctx.author.id, cat_id)
        main_cat = DBManager().user_get_maincat(ctx.author.id)
        if not response:
            embed = discord.Embed(title="💣 Chat introuvable",
                                  description=f"L'id spécifié n'existe pas.\n L'id de vos chats peut-être affiché grâce à la commande **{PREFIX}cats après l'emote 🌐",
                                  colour=discord.Colour.red())
        elif main_cat and main_cat[0] == cat_id:
            embed = discord.Embed(title="😼 Compagnon déjà principal",
                                  description=f"**{response[2]}** est déjà ton compagnon principal.\nPour t'occuper de lui, écris la commande **{PREFIX}card**",
                                  colour=discord.Colour.teal())
        else:
            DBManager().user_set_maincat(ctx.author.id, cat_id)
            embed = discord.Embed(title="😺 Nouveau compagnon",
                                  description=f"**{response[2]}** vient de devenir ton chat principal.\nPour t'occuper de lui, écris la commande **{PREFIX}card**",
                                  colour=discord.Colour.gold())

        embed.set_footer(text=f"• Requête de {ctx.author}")
        await ctx.send(embed=embed)

    @commands.check(check_if_registered)
    @commands.command()
    async def rename(self, ctx, cat_id: int, *, name: str):

        # TODO limiter le nombre de caractère

        response = DBManager().get_info_cat(ctx.author.id, cat_id)
        if not response:
            embed = discord.Embed(title="💣 Chat introuvable",
                                  description=f"L'id spécifié n'existe pas.\n L'id de vos chats peut-être affiché grâce à la commande **{PREFIX}cats après l'emote 🌐",
                                  colour=discord.Colour.red())
        elif response[2] == name:
            embed = discord.Embed(title="📖 Nom déjà appliqué",
                                  description=f"Ce chat est déjà nommé **{name}**.\nPour t'occuper de lui, écris la commande **{PREFIX}card**",
                                  colour=discord.Colour.teal())
        else:
            DBManager().user_set_catname(ctx.author.id, cat_id, name)
            embed = discord.Embed(title="😺 Nouveau nom",
                                  description=f"**{response[2]}** vient d'être renommer **{name}**.\nPour t'occuper de lui, écris la commande **{PREFIX}card**",
                                  colour=discord.Colour.gold())

        embed.set_footer(text=f"• Requête de {ctx.author}")
        await ctx.send(embed=embed)
        
        
    async def _main_shop_choice(self, paginator: dict) -> int:
        main_shop_content = ["La meilleure nourriture afin de satisfaire pleinement l'appétit votre félin.",
                   "Nos poissons du jours afin d'appâter tous les chats que vous rencontrerez.",
                   "Notre sélection de jouets approuvés par le comité des chats entêtés."]
        paginator.builder.base_embed_create(f"🏪 Bienvenue dans Cat 'n' Relax!",
                                f"❓ Pour naviguer entre les articles, utilises les différentes réactions.",
                                discord.Colour.gold())
        
        paginator.builder.content = main_shop_content
        paginator.builder.prefix = list(map(lambda x: str(self.client.get_emoji(x)), [EMOTE_FOOD, EMOTE_FISH, EMOTE_TOY]))
        
        paginator.builder.content_builder(decorator="  ")
        paginator.builder.paginator_store()
        paginator.validation = False
        
        if not await paginator.paginator_emote():
            return
        return paginator.index
    
    async def _sub_shop_choice(self, paginator: dict, products: list, info: tuple, sub_info: str) -> str:
        
        content = [f"x{quantity} {info[id_-1][1].EMOTE}{name.capitalize()} - "
            f"PRIX: **{info[id_-1][1].PRICE}** {str(self.client.get_emoji(EMOTE_MONEY))} / {sub_info}: **{info[id_-1][1].MODIFICATION}**."\
            for id_, name, quantity in products]
        stock = [1 if quantity else 0 for _, _, quantity in products]
        
        compress_content = [c for c, s in zip(content, stock) if s] or "😖 Désolé, nous sommes en rupture général... Revenez demain!"
        compress_products = [f for f, s in zip(products, stock) if s]
        

        paginator.builder.content = compress_content
        paginator.builder.prefix = "/emote/"
        
        paginator.builder.content_builder(decorator=" ➨   ")
        paginator.builder.paginator_store()
        paginator.builder.manager.next_paginator
        paginator.validation = False
        
        result = await paginator.paginator_emote()
        if not result or isinstance(compress_content, str):
            return
        return compress_products[paginator.index]
    
    
    async def product_shop_choice(self, paginator: dict, product: list, info: tuple):
        id_, name, quantity = product
        add_quantity = [-1, -5, -10, -50, -100, 1, 5, 10, 50, 100]
        local_quantity = 1
        
        ### FICTIONNAL SHOP ###
        paginator.builder.paginator_store()
        paginator.builder.manager.next_paginator
        paginator.builder.prefix = "/number/"
        paginator.validation = True
        current_paginator_index = paginator.builder.manager.paginator_index
        ### FICTIONNAL SHOP ###
        
        while True:
            local_add_quantity = [i for i in add_quantity if i > 0 and local_quantity+i <= quantity or i < 0 and local_quantity+i >= 1]
            if not local_add_quantity: break # * There is only one product left in the stock
            
            paginator.builder.base_embed_create(f"💳 Achat de {name}",
                                        f"🛒 Total d'achat: {local_quantity} {name}(s) pour {info[id_-1][1].PRICE * local_quantity} {str(self.client.get_emoji(EMOTE_MONEY))}",
                                        discord.Colour.gold())
            paginator.builder.content = [f"Ajouter {i} {name} au panier." if i > 0 else f"Supprimer {i} {name} du panier." for i in local_add_quantity]
            paginator.builder.content_builder(decorator=" ➨   ")
            paginator.builder.manager[current_paginator_index] = paginator.builder.__dict__ # * Replace old shop product
            
            result = await paginator.paginator_message()
            if result == "V": break
            if not result: return
            
            result_index = paginator.index
            local_quantity += local_add_quantity[result_index]
            
        return local_quantity

    def _update_shop_db(self, author_id, price, quantity, id_, index):
        
        DBManager().user_add_money(author_id, -price*quantity)
        if index == 0:
            DBManager().user_add_food(author_id, f"{quantity}/{id_}")
            DBManager().add_food_stock(-quantity, id_)
        elif index == 1:
            DBManager().user_add_fish(author_id, f"{quantity}/{id_}")
            DBManager().add_fish_stock(-quantity, id_)
        elif index == 2:
            DBManager().user_add_toy(author_id, f"{quantity}/{id_}")
            DBManager().add_toy_stock(-quantity, id_)
            
    async def _send_shop_confirmation(self, author_id, product, info, quantity):
        id_, name, _ = product  
        embed = discord.Embed(title="💰 Nouvel achat!",
                              description=f"{info[id_-1][1].EMOTE} Vous venez d'acheter {quantity} {name}(s) pour {info[id_-1][1].PRICE * quantity} {str(self.client.get_emoji(EMOTE_MONEY))}.",
                              colour=discord.Colour.random())
        user = await self.client.fetch_user(author_id)
        await user.send(embed=embed)
        
            
    @commands.check(check_if_registered)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def shop(self, ctx):


        paginator = PaginatorController(self.client, ctx.author, ctx.channel)
        paginator.builder = PaginatorBuilder()
        
        while True:
            paginator.builder.manager.reset_paginator
            user_choice_index = await self._main_shop_choice(paginator)
            
            if user_choice_index == 0:            
                db_products = DBManager().get_food_stock()
                info_product = get_foods()
                sub_info = "SATURATION"
                paginator.builder.base_embed_create("🍗 Nos stocks de nourriture.",
                                          "🛒 Venez vite, nos stocks partent vite!",
                                          discord.Colour.gold())
                
            elif user_choice_index == 1:
                db_products = DBManager().get_fish_stock()
                info_product = get_fishes()
                sub_info = "ATTRACTION"
                paginator.builder.base_embed_create("🎣 Nos stocks de poissons.",
                                          "🛒 Venez vite, nos stocks partent vite!",
                                          discord.Colour.gold())
            
            elif user_choice_index == 2:
                db_products = DBManager().get_toy_stock()
                info_product = get_toys()
                sub_info = "SATISFACTION"
                paginator.builder.base_embed_create("🧸 Nos stocks de jouets.",
                                          "🛒 Venez vite, nos stocks partent vite!",
                                          discord.Colour.gold())
            else:
                break
            
            user_choice_product = await self._sub_shop_choice(paginator, db_products, info_product, sub_info)
            if not user_choice_product:
                continue
            
            product_quantity = await self.product_shop_choice(paginator, user_choice_product, info_product)
            if not product_quantity:
                continue
            
            self._update_shop_db(author_id=ctx.author.id, price=info_product[user_choice_product[0]-1][1].PRICE,
                                 quantity=product_quantity, id_=user_choice_product[0], index=user_choice_index)
            await self._send_shop_confirmation(ctx.author.id, user_choice_product, info_product, product_quantity)
        
        await paginator.message.delete()
        
    @commands.check(check_if_registered)
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def card(self, ctx):

        main_cat = DBManager().user_get_maincat(ctx.author.id)
        if not main_cat:
            embed = discord.Embed(title="💣 Aucun compagnon principal",
                                  description=f"Pour mettre un chat en compagnon principal faites {PREFIX}main <id>\n L'id de vos chats peut-être affiché grâce à la commande **{PREFIX}cats après l'emote 🌐",
                                  colour=discord.Colour.red())
            embed.set_footer(text=f"• Requête de {ctx.author}")
            await ctx.send(embed=embed, delete_after=60)
            return
        
        response = DBManager().get_info_cat(ctx.author.id, main_cat[0])[2:]
        cat = Cat(*reformat_db_cat(response), main_cat[0], ctx.author.id)
        
        card = await Card(self.client, cat, "among").get_card()
        
        with BytesIO() as image_binary:
            card.save(image_binary, 'PNG')
            image_binary.seek(0)
            filename = f'{cat.name}#{cat.cat_id}_card.png'
            file = discord.File(fp=image_binary, filename=filename)
            
            
        paginator = PaginatorController(self.client, ctx.author, ctx.channel)
        paginator.builder = PaginatorBuilder()
        
        paginator.builder.base_embed_create(f"🏆 Chats de {ctx.author}",
                            f"❓ Pour plus d'information sur un de vos chats, écrivez le chiffre correspondant à celui-ci.",
                            discord.Colour.gold(),
                            field=[["📈 Niveau:", "Ordre décroissant", True], ["💎 Rarité:", "Ordre décroissant", True], ["\u200b", "\u200b", True]],
                            image=filename)
        
        paginator.builder.prefix = "/number/"
        paginator.builder.content = content
        paginator.builder.content_builder(decorator=" ➨ ")
        paginator.builder.paginator_store()
        
        result = await paginator.paginator_message()
        await paginator.message.delete()
        if not result: return
                
        
        
        

def setup(client):
    client.add_cog(CatCommands(client))

# TODO A chaque nouveau chat, mettre une reaction pour modif le nom du chat puis faire un wait pour une entrée pendant 60 secondes
# TODO random suffixe
# TODO su suffixe: "(<RARITY>)"    
# TODO mette la quantité restante du shop dans db
# TODO edit ,cats "ce chat fait partit de votre equipe"
