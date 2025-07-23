from discord import app_commands
import discord
from discord.ui import View, Button, Select, Modal, TextInput


description = """
Add task to backlog
"""

class BacklogModal(Modal):
    task_title = TextInput(
        label='Title',
        placeholder="Enter task title",
        style=discord.TextStyle.short,
        required=True,
        default="New Task",
    )
    task_description = TextInput(
        label='description',
        placeholder="Enter task description, feel free to use markdown",
        style=discord.TextStyle.long,
        required=True,
    )
    story_point = TextInput(
        label='Story Point',
        placeholder="Enter story point for the task",
        style=discord.TextStyle.short,
        required=False,
        default="0",
    )
    
    def __init__(self, interaction, title):
        super().__init__(title=title)
        self.interaction = interaction

    def task_embed(self, user: discord.User):
        embed = discord.Embed(
            title=self.task_title.value,
            description=self.task_description.value,
            color=0x2ecc71,
        )
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.set_footer(text="Added")
        embed.add_field(name="Story Point", value=self.story_point.value, inline=False)
        embed.timestamp = discord.utils.utcnow()
        return embed
    
    async def on_submit(self, interaction):
        message = await interaction.response.send_message(
            embed=self.task_embed(interaction.user),
        )
        message = await interaction.client.get_channel(interaction.channel_id).fetch_message(message.message_id)
        thread = await message.create_thread(
            name=f"Task: {self.task_title.value}",
            auto_archive_duration=60,
            reason="Task discussion thread created",
        )
        await message.edit(embed=message.embeds[0].add_field(
            name="Discussion Thread",
            value=f"<#{thread.id}>" if thread else "",
            inline=False
            )   
        )
        await thread.send(embed=message.embeds[0])
        await message.delete()
        final_message = await interaction.client.get_channel(interaction.channel_id).send(
            embed=message.embeds[0]
        )
        await final_message.add_reaction('⏳')
        await final_message.add_reaction('📝')
        await final_message.add_reaction('✅')

@app_commands.command(name='task', description=description)
async def task(interaction: discord.Interaction):
    guild = interaction.client.get_guild(interaction.guild_id)
    await interaction.response.send_modal(
        BacklogModal(
            interaction=interaction,
            title=f"Add task to {guild.name} backlog"
        )
    )
