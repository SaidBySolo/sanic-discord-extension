from typing import Any, Optional
from sanic_discord.discord.embeds import Embed
from sanic.response import HTTPResponse, json


class Response:
    def make_send(
        self,
        content: Optional[str] = None,
        *,
        embed: Optional[Embed] = None,
        ephemeral: bool = False,
        component: Optional[dict[str, Any]] = None,
    ) -> HTTPResponse:
        res: dict[str, Any] = {"type": 4, "data": {}}

        if content:
            res["data"]["content"] = content
        if embed:
            res["data"]["embeds"] = [embed.to_dict()]

        if ephemeral:
            res["data"].update({"flags": 1 << 6})

        if component:
            res["data"].update(component)

        return json(res)
