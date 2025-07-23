from discord import app_commands
import discord


description = """
Syncs the command tree for current server. Must be admin to use.
"""

@app_commands.command(name='sync', description=description)
async def sync(interaction: discord.Interaction):
    guild = interaction.client.get_guild(interaction.guild_id)
    await interaction.response.send_message("Syncing...", ephemeral=True)
    await interaction.client.tree.sync(guild=guild)
    await interaction.edit_original_response(content=f"Synced {guild.name}")

    