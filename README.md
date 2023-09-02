# echo-python

echo is a toy microservice built with gRPC and SQLAlchemy

## Quickstart

To start the gRPC server listening for incoming requests:

```bash
python src/echo_service_rpc.py
```

To send a request to the server using the gRPC client:

```bash
python src/echo_client.py 'Hello, World!'
```

To start the HTTP-to-gRPC proxy listening for incoming requests:

```bash
python src/echo_proxy.py
```

To send a HTTP POST request to the proxy:

```bash
curl -X POST -d 'Hello, World!' -H 'Content-Type: text/plain' http://localhost:8081/echo
```
