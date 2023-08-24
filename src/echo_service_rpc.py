import dataclasses
import concurrent

import grpc

import echo_pb2
import echo_pb2_grpc
import echo_service


@dataclasses.dataclass
class EchoServiceRpc(echo_pb2_grpc.EchoServiceServicer):
    """
    RPC service implementation that handles remote procedure calls related to the Echo service.
    It leverages the human-friendly interface defined in echo_service.EchoService.

    :param service: The underlying EchoService that implements the core logic.
    """

    service: echo_service.EchoService

    def echo(
        self, request: echo_pb2.EchoRequest, context: grpc.ServicerContext
    ) -> echo_pb2.EchoResponse:
        """
        Implementation of the Echo RPC method. It delegates the actual logic to the EchoService,
        thus maintaining a separation between the RPC layer and the service logic.

        :param request: The EchoRequest object containing the message to be echoed.
        :return: The EchoResponse object containing the echoed message.
        """
        # Retrieve the message from the request
        message = self.service.echo(request.message)

        # Build and return the response by encapsulating the echoed message
        return echo_pb2.EchoResponse(message=message)


@dataclasses.dataclass
class EchoServer:
    """
    Server class configured to run on port 8080 and to handle RPC requests using the
    EchoServiceRpc class, which delegates the requests to the EchoService implementation.
    """

    echo_service_instance: echo_service.EchoService

    def __post_init__(self) -> None:
        # Server instance
        self.server: grpc.Server = grpc.server(
            concurrent.futures.ThreadPoolExecutor(max_workers=10)
        )
        echo_pb2_grpc.add_EchoServiceServicer_to_server(
            EchoServiceRpc(self.echo_service_instance), self.server
        )
        self.server.add_insecure_port("[::]:8080")

    def start(self) -> None:
        """
        Starts the gRPC server, enabling it to accept incoming connections and RPC requests.
        It prints a message to the console indicating that the server is listening on port 8080,
        and then it blocks until the server is terminated.
        """
        # Starting the server
        self.server.start()
        print("Server started, listening on 8080")
        self.server.wait_for_termination()


if __name__ == "__main__":
    # Creating an instance of the EchoService
    echo_service_instance = echo_service.EchoService()

    # Creating an instance of the EchoServer class
    echo_server = EchoServer(echo_service_instance)

    # Starting the server
    echo_server.start()
