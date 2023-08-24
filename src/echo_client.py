import dataclasses
import sys

import grpc

import echo_pb2
import echo_pb2_grpc


@dataclasses.dataclass
class EchoClient:
    """
    Client implementation for the Echo service that sends RPC requests to the server.
    It constructs the RPC request and handles the response.

    :param channel: The gRPC Channel used to communicate with the server.
    """

    channel: grpc.Channel

    def __post_init__(self) -> None:
        # Create a stub (client proxy) using the provided channel
        self.rpc = echo_pb2_grpc.EchoServiceStub(self.channel)

    def echo(self, message: str) -> str:
        """
        Sends an echo request to the server with the provided message, and returns the echoed message.

        :param message: The message to be echoed.
        :return: The echoed message received from the server.
        """
        # Build the EchoRequest object using the provided message
        request = echo_pb2.EchoRequest(message=message)

        # Send the request to the server and return the echoed message
        response = self.rpc.echo(request)
        return response.message


if __name__ == "__main__":
    # Entry point for the client application.

    # Create a channel to the server running on localhost at port 8080
    channel = grpc.insecure_channel("localhost:8080")

    # Create a client instance using the channel
    client = EchoClient(channel)

    # Retrieve the message from the command-line arguments or use a default message
    message = sys.argv[1] if len(sys.argv) > 1 else "default-message"

    # Send the message to the server and print the response
    response = client.echo(message)
    print(f"Server responded with: {response}")

    # Shutdown the channel
    channel.close()
