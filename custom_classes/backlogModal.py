import discord
from discord.ui import Modal, TextInput

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
    
    def __init__(self, interaction: discord.Interaction, title: str):
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
    
    async def on_submit(self, interaction: discord.Interaction):
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


class prefilledBacklogModal(BacklogModal):
    def __init__(self, interaction: discord.Interaction, message: discord.Message):
        super().__init__(interaction, title=f"Editing Task {message.embeds[0].title}")
        self.message = message
        self.embed = message.embeds[0]
        self.task_title.default = self.embed.title
        self.task_description.default = self.embed.description
        self.story_point.default = self.embed.fields[0].value if self.embed.fields else "0"

    async def on_submit(self, interaction: discord.Interaction):
        new_embed = self.task_embed(interaction.user)
        # Find the value for the field with name "Discussion Thread"
        thread_value = None
        for field in self.embed.fields:
            if field.name == "Discussion Thread":
                thread_value = field.value
                break

        if thread_value and thread_value.startswith('<#') and thread_value.endswith('>'):
            thread_id = int(thread_value[2:-1])
            thread = interaction.client.get_channel(thread_id)
            new_embed.add_field(
                name="Discussion Thread",
                value=thread_value,
                inline=False
            )
        else:
            thread = None
            new_embed.add_field(
                name="Discussion Thread",
                value="No discussion thread",
                inline=False
            )

        await self.message.edit(embed=new_embed)
        if thread:
            await thread.send(content="Task edited", embed=new_embed)
        
        await interaction.response.send_message(
            content="Task updated successfully!",
            ephemeral=True
        )