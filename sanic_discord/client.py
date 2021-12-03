from typing import NoReturn, cast

from nacl.exceptions import BadSignatureError  # type: ignore
from nacl.signing import VerifyKey  # type: ignore
from sanic.app import Sanic
from sanic.exceptions import Unauthorized
from sanic.response import json

from sanic_discord.discord.interactions import Interaction
from sanic_discord.discord.types.interactions import ApplicationCommandInteractionData
from sanic_discord.http import DiscordBaseHTTP
from sanic_discord.register import RegisterCommand, RegisterdInfo
from sanic_discord.typing import SanicDiscordRequest
from sanic_discord.response import Response


class Handler:
    commands: dict[str, RegisterdInfo] = {}

    def __init__(
        self,
        app: Sanic,
        client_public_key: str,
        token: str,
        uri: str = "discord_interaction",
        production: bool = False,
    ) -> None:
        self.app = app
        self.uri = uri
        self.token = token
        self.client_public_key = client_public_key

        self.__setup()

    def __setup(self):
        self.app.add_route(self.__handler, self.uri, ["POST"])

        # Injection
        self.app.ctx.http = DiscordBaseHTTP(self.token)
        self.app.ctx.response = Response()

    def command_register(self, info: RegisterCommand):
        self.commands.update({info.registerd_info.name: info.registerd_info})

    @staticmethod
    def verify_signiture(
        raw_body: bytes, signature: str, timestamp: str, client_public_key: str
    ):
        message = timestamp.encode() + raw_body
        try:
            vk = VerifyKey(bytes.fromhex(client_public_key))
            vk.verify(message, bytes.fromhex(signature))  # type: ignore
            return True
        except BadSignatureError:
            return False

    async def __handler(self, request: SanicDiscordRequest):
        signature = request.headers.get("X-Signature-Ed25519")
        timestamp = request.headers.get("X-Signature-Timestamp")
        if (
            signature
            and timestamp
            and self.verify_signiture(
                request.body, signature, timestamp, self.client_public_key
            )
        ):
            if request.json["type"] == 1:
                return json({"type": 1})

            if request.json["type"] == 2:
                return await self.dispatch_application_command(request)

            if request.json["type"] == 3:
                return await self.dispatch_message_component(request)

        raise Unauthorized("not_verified", 401)

    async def dispatch_application_command(self, request: SanicDiscordRequest):
        interaction = Interaction(request.json)
        if interaction.data:
            interaction_data = cast(ApplicationCommandInteractionData, interaction.data)

            # Handle Subcommand
            if interaction_data.get("type") == 1:
                if interaction_data["name"] in self.commands:
                    command = self.commands[interaction_data["name"]]
                    if interaction_options := interaction_data.get("options"):
                        option = interaction_options[0]
                        if option["name"] in command.sub_command:
                            sub_command_func = command.sub_command[option["name"]]
                            request.ctx.interaction = interaction
                            return await sub_command_func(
                                request,
                                *tuple(map(lambda x: x["value"], option["options"])),  # type: ignore
                            )

                    interaction_data.get("type")

            # TODO: Handle Subcommand Group

    async def dispatch_message_component(
        self, request: SanicDiscordRequest
    ) -> NoReturn:
        raise NotImplementedError
