import discord
from discord import app_commands
from custom_classes.backlogModal import prefilledBacklogModal


description = """
edit tasks
"""

@app_commands.command(name='edit', description=description)
async def edit(interaction: discord.Interaction, task: str):
    message = await interaction.client.get_channel(interaction.channel_id).fetch_message(int(task))
    await interaction.response.send_modal(
        prefilledBacklogModal(
            interaction=interaction,
            message=message,
        )
    )

@edit.autocomplete('task')
async def edit_autocomplete(interaction: discord.Interaction, current: str):
    channel = interaction.client.get_channel(interaction.channel_id)

    options = []
    async for message in channel.history(limit=None):
        if message.author.bot and message.embeds and message.embeds[0].author.name == interaction.user.name:
            options.append(
                app_commands.Choice(
                    name=message.embeds[0].title,
                    value=str(message.id)
                )
            )
    if current == '':
        return options[:25]
    else:
        return [option for option in options if current.lower() in option.name.lower()][:25]

            
