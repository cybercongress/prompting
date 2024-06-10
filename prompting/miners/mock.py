# The MIT License (MIT)
# Copyright © 2024 Yuma Rao
# Copyright © 2024 cyber~Congress

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import typing
from functools import partial
from starlette.types import Send

# Cybertensor Miner Template:
from prompting.protocol import StreamPromptingSynapse

# import base miner class which takes care of most of the boilerplate
from prompting.base.prompting_miner import BaseStreamPromptingMiner


class MockMiner(BaseStreamPromptingMiner):
    """
    This little fella responds with a static message.
    """

    def __init__(self, config=None):
        super().__init__(config=config)

    def forward(self, synapse: StreamPromptingSynapse) -> StreamPromptingSynapse:
        async def _forward(message: str, send: Send):
            await send(
                {
                    "type": "http.response.body",
                    "body": message,
                    "more_body": False,
                }
            )

        message = f"Hey you reached mock miner {self.config.wallet.hotkey!r}. Please leave a message after the tone.. Beep!"
        token_streamer = partial(_forward, message)
        return synapse.create_streaming_response(token_streamer)

    async def blacklist(
        self, synapse: StreamPromptingSynapse
    ) -> typing.Tuple[bool, str]:
        return False, "All good here"

    async def priority(self, synapse: StreamPromptingSynapse) -> float:
        return 1e6
