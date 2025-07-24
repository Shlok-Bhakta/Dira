import discord
import time
import traceback
import json
import datetime
import os
from bot_commands import COMMANDS
from bot_events.reactions import handle_raw_reaction_add


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = int(time.time())
        self.tree = discord.app_commands.CommandTree(self)
        self.channels = {
            "backlog": 1397406490083594403,
            "todo": 1397406522929184841,
            "doing": 1397406542000685166,
            "done": 1397406553090429071,
        }

    async def setup_hook(self) -> None:
        await self.init_commands()

    async def on_ready(self):
        self.COMMANDS = await self.tree.fetch_commands()
        self.COMMANDS = {command.name: command for command in self.COMMANDS}

        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_error(self, event_method, /, *args, **kwargs):
        with open('error_log.txt', 'w') as f:
            f.write(f"{traceback.format_exc()}")
        return await super().on_error(event_method, *args, **kwargs)
    
    async def init_commands(self):
        for command in COMMANDS:
            self.tree.add_command(command)
            print(f"Command {command.name} initialized.")
    
    async def on_raw_reaction_add(self, payload):
        await handle_raw_reaction_add(self, payload, self.channels)

