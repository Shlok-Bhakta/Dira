from discord import app_commands
import discord


description = """
Purge message from channel, must be admin to use.
"""

@app_commands.command(name='purge_message', description=description)
async def purge_message(interaction: discord.Interaction, num_messages: int = 10):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
        return

    channel = interaction.channel
    if not channel:
        await interaction.response.send_message("Channel not found.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    deleted_messages = await channel.purge(limit=num_messages)
    await interaction.followup.send(f"Deleted {len(deleted_messages)} messages from {channel.mention}.", ephemeral=True)    