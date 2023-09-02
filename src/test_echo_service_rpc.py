import concurrent
import grpc

import echo_log_store
import echo_pb2
import echo_pb2_grpc
import echo_service_rpc
import echo_service


class TestEchoServiceRpc:
    server: grpc.Server
    port: int
    channel: grpc.Channel

    @classmethod
    def setup_class(cls) -> None:
        # Create server
        cls.server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))
        echo_pb2_grpc.add_EchoServiceServicer_to_server(
            echo_service_rpc.EchoServiceRpc(
                echo_service.EchoService(echo_log_store.EchoLogStore())
            ),
            cls.server,
        )

        # Bind to a real port
        cls.port = cls.server.add_insecure_port(
            "localhost:0"
        )  # Bind to an available port
        cls.server.start()

        # Create channel
        cls.channel = grpc.insecure_channel(f"localhost:{cls.port}")

    @classmethod
    def teardown_class(cls) -> None:
        # Shutdown channel and server after test execution
        cls.channel.close()
        cls.server.stop(None)

    def test_echo_rpc(self) -> None:
        # Arrange: Define request message
        message = "Hello, World!"
        request = echo_pb2.EchoRequest(message=message)

        # Act: Invoke RPC call and get the response
        stub = echo_pb2_grpc.EchoServiceStub(self.channel)
        response = stub.echo(request)

        # Assert: Verify that the response is as expected
        expected_response = echo_pb2.EchoResponse(message="13:" + message)
        assert expected_response == response
