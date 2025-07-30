"""
This boi is going to take audio from discord channel and summarize it
"""

import datetime
import discord
import requests
import base64
import dotenv
import os

async def handle_on_message(bot: discord.Client, message: discord.Message):
    # check if message is in the standup channel
    if message.channel.id != bot.channels["stand-up"]:
        return

    # check if message is a voice message
    if not message.attachments:
        print("Message is not a voice message")
        return
    
    # pull the audio file from the message attachment.url
    audio_file = requests.get(message.attachments[0].url, timeout=10)

    # Convert audio bytes to base64
    audio_base64 = base64.b64encode(audio_file.content).decode('utf-8')
    
    # Get the file extension to determine MIME type
    filename = message.attachments[0].filename.lower()
    if filename.endswith('.mp3'):
        mime_type = "audio/mp3"
    elif filename.endswith('.wav'):
        mime_type = "audio/wav"
    elif filename.endswith('.ogg'):
        mime_type = "audio/ogg"
    elif filename.endswith('.m4a'):
        mime_type = "audio/mp4"
    else:
        mime_type = "audio/mpeg"  # default
    
    # Prepare the request to Gemini API
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": """
                        you are a bot who is going to summarize standup meeting audio.
                        the output should be as follows:

                        ## Standup Summary
                        This is a summary of the standup meeting. keep it as short as possible while still conveying the main points.

                        ## Key Points
                        - point 1
                        - point 2
                        - point 3
                        ... use as many points as you want

                        ## Blockers
                        - blocker 1
                        - blocker 2
                        - blocker 3
                        ... use as many blockers as you want

                        keep it simple, remember the goal is a summary not a story
                        """
                    },
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": audio_base64
                        }
                    }
                ]
            }
        ]
    }
    dotenv.load_dotenv()
    response = requests.post(
        f"{gemini_url}?key={os.getenv('GEMINI_API')}",
        headers=headers,
        json=payload,
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        summary = result["candidates"][0]["content"]["parts"][0]["text"]
        
        # Send the summary back to Discord
        embed = discord.Embed.from_dict({
            "title": f"{message.author.display_name} Standup Summary",
            "description": f"{summary}",
            "color": 0x82efc2,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": message.author.display_name,
                "icon_url": message.author.display_avatar.url,
            },
            "thumbnail": {
                "url": message.author.display_avatar.url,
            },
        })
        await message.reply(embed=embed)
        print(f"Summary generated: {summary}")
    else:
        print(f"Error from Gemini API: {response.status_code} - {response.text}")
        # Send the summary back to Discord
        embed = discord.Embed.from_dict({
            "title": f"{message.author.display_name} Standup Summary FAILED",
            "description": f"{summary}",
            "color": 0x500000,
            "timestamp": datetime.datetime.now().isoformat(),
            "author": {
                "name": message.author.display_name,
                "icon_url": message.author.display_avatar.url,
            },
            "thumbnail": {
                "url": message.author.display_avatar.url,
            },
        })

        await message.reply(embed=embed)


    print(f"Attachments: {message.attachments}")