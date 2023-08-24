import dataclasses

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
