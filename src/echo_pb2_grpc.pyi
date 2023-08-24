import grpc
from grpc import Channel, UnaryUnaryMultiCallable
from echo_pb2 import EchoRequest, EchoResponse

class EchoServiceServicer:
    def echo(
        self, request: EchoRequest, context: grpc.ServicerContext
    ) -> EchoResponse: ...

def add_EchoServiceServicer_to_server(
    servicer: EchoServiceServicer, server: grpc.Server
) -> None: ...

class EchoServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    echo: UnaryUnaryMultiCallable[EchoRequest, EchoResponse]
