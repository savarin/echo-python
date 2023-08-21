class EchoService:
    """
    Service implementation that handles the echoing of messages. It transforms the input by
    prefixing the length of the original message, followed by the message itself.
    """

    def echo(self, message: str) -> str:
        """
        Echoes the input message with a specific format. It calculates the length of the input
        message and prefixes it to the original message.

        Args:
            message: The input message to be echoed.

        Returns:
            The transformed message containing the length followed by the original message.
        """
        return f"{len(message)}:{message}"
