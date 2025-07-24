from discord import app_commands
import discord
from custom_classes.backlogModal import BacklogModal

description = """
Add task to backlog
"""

@app_commands.command(name='task', description=description)
async def task(interaction: discord.Interaction):
    await interaction.response.send_modal(
        BacklogModal(
            interaction=interaction,
            title=f"Add task to {interaction.channel.name}"
        )
    )
