import discord
import os
from DiscordClient import MyClient
from dotenv import load_dotenv


intents = discord.Intents.default()
intents.members = True
intents.message_content=True

client = MyClient(
    intents=intents, 
    allowed_mentions=discord.AllowedMentions(
        everyone=False, 
        users=True, 
        roles=True, 
        replied_user=True
    ),
)

load_dotenv()
client.run(os.getenv('TOKEN'))
