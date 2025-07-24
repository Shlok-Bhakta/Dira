from discord import app_commands
import discord
import time

description = """
Syncs the command tree for current server. Must be admin to use.
"""

@app_commands.command(name='sync', description=description)
async def sync(interaction: discord.Interaction):
    start = time.time()
    await interaction.response.send_message("Syncing commands...")
    await interaction.client.tree.sync(guild=None)
    await interaction.edit_original_response(
        content=f"Commands synced in {time.time() - start:.2f} seconds."
    )
