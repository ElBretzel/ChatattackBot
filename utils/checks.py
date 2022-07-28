from utils.database import DBManager
from utils.error_handler import ErrorNotRegistered, ErrorNoMainCat

def check_if_registered(ctx):
    if DBManager().check_if_user_exists(ctx.author.id):
        return True
    raise ErrorNotRegistered

def check_if_main_exist(ctx):
    if DBManager().user_get_maincat(ctx.author.id):
        return True
    raise ErrorNoMainCat