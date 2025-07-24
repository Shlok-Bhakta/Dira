from .status import status
from .sync import sync
from .add_backlog import task
from .purge_message import purge_message
from .edit import edit

COMMANDS = [status, sync, task, purge_message, edit]