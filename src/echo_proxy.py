import flask
import grpc

import echo_pb2
import echo_pb2_grpc

# Initialize Flask app
app = flask.Flask(__name__)

# Create a gRPC channel and stub
channel = grpc.insecure_channel('localhost:8080')
stub = echo_pb2_grpc.EchoServiceStub(channel)

@app.route('/echo', methods=['POST'])
def echo():
    """
    HTTP POST endpoint for the /echo route that forwards requests to the gRPC service.
    """
    # Retrieve the message from the request body
    message = flask.request.data.decode("utf-8")

    # Build the EchoRequest object using the retrieved message
    echo_request = echo_pb2.EchoRequest(message=message)

    # Invoke the echo method on the stub and get the response
    response = stub.echo(echo_request)

    # Return the response message as the HTTP response
    return response.message

# Run the Flask app on port 8081
if __name__ == '__main__':
    app.run(port=8081)
