from discord.ext.commands import CheckFailure

from constants import PREFIX


class CatAttackError:
    
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return self.message

class ErrorPaginatorCharacter(CatAttackError, CheckFailure):
    def __init__(self):
        super().__init__(message = "📛 Impossible d'envoyer le message.\nLe message dépasse les 2000 caractères...")


class ErrorNotRegistered(CatAttackError, CheckFailure):
    def __init__(self):
        super().__init__(message = f"😨 Vous n'avez pas encore créé de compte!\nPour créer un compte, écrivez dans un salon du serveur **{PREFIX}register**")
        
class ErrorNoMainCat(CatAttackError, CheckFailure):
    def __init__(self):
        super().__init__(message = f"😿 Aucun compagnon principal paramétré.\nPour paramétrer un compagnon principal, écrivez dans un salon du serveur **{PREFIX}main_cat")