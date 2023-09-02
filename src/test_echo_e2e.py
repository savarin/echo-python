from typing import Generator, Tuple
import concurrent.futures
import grpc
import pytest
import echo_pb2
import echo_pb2_grpc
import echo_service
import echo_service_rpc
import echo_log_store


@pytest.fixture(scope="module")
def grpc_server() -> Generator[Tuple[grpc.Server, int], None, None]:
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
    echo_pb2_grpc.add_EchoServiceServicer_to_server(
        echo_service_rpc.EchoServiceRpc(
            echo_service.EchoService(echo_log_store.EchoLogStore())
        ),
        server,
    )
    port = server.add_insecure_port("localhost:0")
    server.start()
    yield server, port
    server.stop(None)


@pytest.fixture(scope="module")
def grpc_channel(
    grpc_server: Tuple[grpc.Server, int]
) -> Generator[grpc.Channel, None, None]:
    _, port = grpc_server
    channel = grpc.insecure_channel(f"localhost:{port}")
    yield channel
    channel.close()


def test_echo(grpc_channel: grpc.Channel) -> None:
    # Arrange
    pre_size = len(echo_log_store.EchoLogStore().get_all())
    stub = echo_pb2_grpc.EchoServiceStub(grpc_channel)
    request = echo_pb2.EchoRequest(message="foo")

    # Act
    response = stub.echo(request)

    # Assert
    assert response.message == "3:foo"
    post_size = len(echo_log_store.EchoLogStore().get_all())
    assert pre_size + 1 == post_size
