from typing import Generator, Tuple
import concurrent.futures

import grpc
import pytest

import echo_log_store
import echo_pb2
import echo_pb2_grpc
import echo_service
import echo_service_rpc


# pytest fixture for setting up the gRPC server
@pytest.fixture(scope="module")
def grpc_server() -> Generator[Tuple[grpc.Server, int], None, None]:
    """
    Sets up a gRPC server for testing purposes.
    Configures the EchoService and starts the server, yielding control back for testing.
    After tests are done, the server is stopped.
    """
    # Create the server with a ThreadPoolExecutor
    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    # Add EchoService to server
    echo_pb2_grpc.add_EchoServiceServicer_to_server(
        echo_service_rpc.EchoServiceRpc(
            echo_service.EchoService(echo_log_store.EchoLogStore())
        ),
        server,
    )

    # Bind to an available port
    port = server.add_insecure_port("localhost:0")
    server.start()

    # Yield server and port for testing
    yield server, port

    # Stop the server after tests
    server.stop(None)


# pytest fixture for setting up the gRPC client channel
@pytest.fixture(scope="module")
def grpc_channel(
    grpc_server: Tuple[grpc.Server, int]
) -> Generator[grpc.Channel, None, None]:
    """
    Sets up a gRPC channel for testing purposes.
    Uses the server and port provided by the grpc_server fixture.
    """
    # Get port from grpc_server fixture
    _, port = grpc_server

    # Create channel to the server
    channel = grpc.insecure_channel(f"localhost:{port}")

    # Yield channel for testing
    yield channel

    # Close the channel after tests
    channel.close()


# Test function for the Echo service's echo() method
def test_echo(grpc_channel: grpc.Channel) -> None:
    """
    Test for the Echo service's RPC method.
    Ensures the message is properly processed and log size increases by one.
    """
    # Arrange: Prepare the state and data before the test
    pre_size = len(echo_log_store.EchoLogStore().get_all())
    stub = echo_pb2_grpc.EchoServiceStub(grpc_channel)
    request = echo_pb2.EchoRequest(message="foo")

    # Act: Perform the action to test
    response = stub.echo(request)

    # Assert: Check the result against expectations
    assert response.message == "3:foo"

    # Verify log size increase
    post_size = len(echo_log_store.EchoLogStore().get_all())
    assert pre_size + 1 == post_size
