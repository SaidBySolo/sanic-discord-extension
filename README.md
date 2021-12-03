# sanic-discord

## Example

server.py

```py
from sanic.app import Sanic

from sanic_discord_extension.client import Handler
from commands.say import say

sanic = Sanic(__name__)

app = Handler(
    sanic,
    "client_pubic_key",
    "Bot token",
)

app.command_register(say)

sanic.run("0.0.0.0", 8000)
```

commands/say.py

```py 
from sanic_discord_extension.register import RegisterCommand, CommandArgument
from sanic_discord_extension.typing import SanicDiscordRequest

say = RegisterCommand(name="say", description="Say anything")

@say.sub_command(
    name="anything",
    description="say anything",
    options=[
        CommandArgument(
            name="word",
            description="word to say",
            type=3,
            required=True,
        ),
    ],
)
async def say_anything(request: SanicDiscordRequest, argument:str):
    return request.app.ctx.response.make_send(f"word: {argument}")
```

## Known issue

### Register

Commands are not automatically registered.

The user must register by using the ``RegisterCommand.to_dict()`` method.

### Component

component not implemented

### Sub command group and command

command and subcommand groups not implemented