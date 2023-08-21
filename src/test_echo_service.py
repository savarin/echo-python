import echo_service


def test_echo_service() -> None:
    service = echo_service.EchoService()
    message = "Hello, World!"

    assert service.echo(message) == "13:Hello, World!"
