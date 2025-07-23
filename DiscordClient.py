import discord
import time
import traceback
import json
import datetime
import os
from bot_commands import COMMANDS


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = int(time.time())
        self.tree = discord.app_commands.CommandTree(self)
        
    async def setup_hook(self) -> None:
        pass

    async def on_ready(self):
        self.COMMANDS = await self.tree.fetch_commands()
        self.COMMANDS = {command.name: command for command in self.COMMANDS}

        await self.sync_commands()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_error(self, event_method, /, *args, **kwargs):
        # Log the error to the ERROR_LOG_CHANNEL
        error_message = f"Error in {event_method} with args {args} and kwargs {kwargs}"
        with open('error_log.txt', 'w') as f:
            f.write(f"{traceback.format_exc()}")
        await self.ERROR_LOG_CHANNEL.send(error_message, file=discord.File('error_log.txt', filename='error_log.txt'))
        os.remove('error_log.txt')
        return await super().on_error(event_method, *args, **kwargs)
    
    async def sync_commands(self):
        for command in COMMANDS:
            self.tree.add_command(command)
        await self.tree.sync()
