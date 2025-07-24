import discord

async def handle_raw_reaction_add(bot: discord.Client, payload: discord.RawReactionActionEvent, channels: dict):
    if payload.user_id == bot.user.id:
        return
    channel = bot.get_channel(payload.channel_id)
    if not channel:
        return

    message = await channel.fetch_message(payload.message_id)
    if not message or message.author.id != bot.user.id:
        return
    
    emoji_lookup = {
        '📝': 'doing',
        '✅': 'done',
        '⏳': 'todo',
        }
    
    destination_channel = channels.get(emoji_lookup.get(payload.emoji.name))
    if not destination_channel:
        return
    destination_channel = bot.get_channel(destination_channel)
    await message.delete()
    new_message = await destination_channel.send(embed=message.embeds[0])
    for emoji in emoji_lookup.keys():
        if emoji != payload.emoji.name:
            await new_message.add_reaction(emoji)
