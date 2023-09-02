import echo_log_store
import echo_service


def test_echo_service() -> None:
    service = echo_service.EchoService(echo_log_store.EchoLogStore())
    message = "Hello, World!"

    assert service.echo(message) == "13:Hello, World!"
