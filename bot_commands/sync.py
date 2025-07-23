from discord import app_commands
import discord


description = """
Syncs the command tree for current server. Must be admin to use.
"""

@app_commands.command(name='sync', description=description)
async def sync(interaction: discord.Interaction):
    await interaction.response.send_message("Syncing commands...")
    await interaction.client.init_commands()
    await interaction.followup.send("Commands synced successfully!")
