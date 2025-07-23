from discord import app_commands
import discord
import datetime

class StatusView(discord.ui.View):
    def __init__(self):
        super().__init__()  
        GithubButton = discord.ui.Button(label='Github', style=discord.ButtonStyle.url, url='https://github.com/Shlok-Bhakta/Dira')
        self.add_item(GithubButton)

def new_embed(client: discord.Client):
    return discord.Embed.from_dict({
        "title": "Status",
        "description": "",
        "color": 0x500000,
        "timestamp": datetime.datetime.now().isoformat(),
        "author": {
            "name": client.user.display_name,
            "icon_url": client.user.display_avatar.url,
        },
        "thumbnail": {
            "url": client.user.display_avatar.url,
        },
        "fields": [
            {"name": "Latency", "value": f"{client.latency * 1000:.1f} ms", "inline": False},
            {"name": "Online Since", "value": f"<t:{client.start_time}:R>", "inline": False},
        ],
    })

description = """
Returns bot's online status.
"""

@app_commands.command(name='status', description=description)
async def status(interaction: discord.Interaction):
    await interaction.response.send_message(embed=new_embed(interaction.client), view = StatusView())