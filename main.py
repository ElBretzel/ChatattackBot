import os
import glob
import sys

from discord import Intents
from discord.ext import commands
import aiocron

from constants import *
from utils.database import DBManager

# Open discord bot token
with open(os.path.join(KEY_DIRECTORY, "discord-key.txt"), "r") as f:
    TOKEN = f.read()

# Set working directory to current file directory
sys.path.insert(1, DIRECTORY)
os.chdir(DIRECTORY)

# Necessary (to detect some events)
default_intents = Intents.default()
default_intents.members = True
default_intents.typing = False
default_intents.presences = False


class Bot(commands.Bot):
    def __init__(self, token, prefix):
        self.token = token
        self.prefix = prefix
        super().__init__(command_prefix = self.prefix, intents = default_intents, reconnect = True)
        
    def load_commands(self):
        # * Import and load all commands (cogs)
        cogs_file = glob.iglob(f"cogs{OS_SLASH}**.py")
        for files in cogs_file:
            files = files.split(f"{OS_SLASH}")[1][:-3]
            print(f"Starting cog {files}")
            self.load_extension(f'cogs.{files}')
    
    def start_bot(self):

        print("\nDeleting help command...")
        self.remove_command('help')
        print("Done!")
        print("Checking database...")
        DBManager()
        print("Done!")
        print("Loading cogs...")
        self.load_commands()
        print("Done!")
        print("Bot launching...")
        self.run(self.token)
        
    async def on_ready(self):
        print("{:-^30}".format(""))
        print("Bot is ready!")
        print(f"Status: {round(self.latency, 3)} ms")
        print("{:-^30}".format(""))
        
if __name__ == "__main__":

    client = Bot(TOKEN, PREFIX)
    client.start_bot()

# TODO uvloop