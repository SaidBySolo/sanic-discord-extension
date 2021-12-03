from types import SimpleNamespace
from typing import Any, Callable, Coroutine, TypeVar

from multidict import CIMultiDict
from sanic.request import Request
from sanic_discord_extension.discord.interactions import Interaction

from sanic_discord_extension.http import DiscordBaseHTTP
from sanic_discord_extension.response import Response

CORO = Callable[..., Coroutine[Any, Any, Any]]

Sanic = TypeVar("Sanic")


class SanicDiscordContext(SimpleNamespace):
    http: DiscordBaseHTTP
    response: Response


class _RequestContext(SimpleNamespace):
    interaction: Interaction


class SanicDiscordSanic:
    ctx: SanicDiscordContext


class SanicDiscordRequest(Request):
    headers: CIMultiDict[Any]
    json: Any
    body: bytes
    ctx: _RequestContext
    app: SanicDiscordSanic
