import sys

from discord import Embed, Colour, errors
from discord.ext import commands
from utils.error_handler import CatAttackError

from constants import PREFIX, DEV

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        if issubclass(type(error), CatAttackError):
            error_splitted = str(error).splitlines()
            embed = Embed(
                title = error_splitted[0], 
                description = error_splitted[1], 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = Embed(
                title = "❓ Argument manquant.", 
                description = f"Il manque un ou plusieurs arguments dans la commande. Pour voir le menu d'aide, faites **{PREFIX}help {ctx.invoked_with}**.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.BadArgument):
            embed = Embed(
                title = "🧹 Argument invalide.", 
                description = f"Un argument a mal été spécifié dans la commande. Pour voir le menu d'aide, faites **{PREFIX}help {ctx.invoked_with}**.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.BotMissingPermissions):
            embed = Embed(
                title = "🤖 Permission invalide.", 
                description = "Le bot manque des permissions afin d'éxecuter certaines actions. Veillez contacter l'administrateur du serveur.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.ChannelNotFound):
            embed = Embed(
                title = "🚪 Salon inexistant.", 
                description = "Le bot n'arrive pas à atteindre le salon spécifié.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.CommandNotFound):
            embed = Embed(
                title = "👀 Commande introuvable.", 
                description = f"Pour voir la liste complète des commandes, faites **{PREFIX}help**.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.CommandOnCooldown):
            embed = Embed(
                title = "⌛️ Commande sous cooldown.", 
                description = f"Réessayer dans quelques secondes.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.EmojiNotFound):
            embed = Embed(
                title = "😖 Emoji introuvable.", 
                description = f"L'emoji spécifié est soit introuvable, soit mal écrit.", 
                color = Colour.red(), 
            )
        elif isinstance(error, (commands.MemberNotFound, commands.UserNotFound)):
            embed = Embed(
                title = "😶 Utilisateur introuvable.", 
                description = f"L'Utilisateur spécifié est soit introuvable, soit mal écrit.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.MessageNotFound):
                embed = Embed(
                title = "🗃 Message introuvable.", 
                description = f"Le message spécifié est soit introuvable, soit mal écrit.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.MissingPermissions):
                embed = Embed(
                title = "🔑 Permission manquante.", 
                description = f"Vous manquez de permission afin d'éxecuter la commande **{ctx.invoked_with}**.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.RoleNotFound):
            embed = Embed(
                title = "🏷 Role introuvable.", 
                description = f"Le role spécifié est soit introuvable, soit mal écrit.", 
                color = Colour.red(), 
            )
        elif isinstance(error, commands.TooManyArguments):
            embed = Embed(
                title = "📏 Trop d'arguments.", 
                description = f"Trop d'arguments ont été spécifié dans la commande. Pour voir le menu d'aide, faites **{PREFIX}help {ctx.invoked_with}**.", 
                color = Colour.red(), 
            )
        else:            
            embed = Embed(
                title = "💥 Erreur inconnue!", 
                description = f"Une erreur est survenue pendant l'éxecution de la **{ctx.invoked_with}**:\n\nType: **{type(error)}**\nMessage: **{error}**\n\nVeillez contactez <@{DEV}>.", 
                color = Colour.red(), 
            )
            
            
        embed.set_footer(text = f"• Serveur: {ctx.guild.name}")
        await ctx.author.send(embed = embed)
        
def setup(client):
    client.add_cog(CommandErrorHandler(client))