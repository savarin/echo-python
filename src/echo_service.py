import dataclasses

import echo_log_entity
import echo_log_store


@dataclasses.dataclass
class EchoService:
    """
    Service implementation that handles the echoing of messages. It transforms the input by
    prefixing the length of the original message, followed by the message itself.
    """

    store: echo_log_store.EchoLogStore

    def echo(self, message: str) -> str:
        """
        Echoes the input message with a specific format. It calculates the length of the input
        message and prefixes it to the original message.

        :param message: The input message to be echoed.
        :return: The transformed message containing the length followed by the original message.
        """

        self.store.insert(echo_log_entity.EchoLogEntity.create(message=message))

        return f"{len(message)}:{message}"
