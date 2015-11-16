"""Create an http server which will always respond with the specified http
status code.

Usage:
    simple_status_server.py --help
    simple_status_server.py <status> [options]

Arguments:
    <status>  The HTTP status code of every response from the server.

Options:
    --port=<port>   The port the server runs on [default: 80]
    --help          Show this help page
    --debug         Enable flask debugging
"""
from docopt import docopt
from flask import Flask, Response
from flask.ext.cors import CORS
from json import dumps

app = Flask(__name__)
CORS(app)

STATUS_KEY = "status"


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def respond(path=None):
    http_status = app.config[STATUS_KEY]
    data = dumps({
        STATUS_KEY: http_status,
        "success": True,
        "message": "ok"
    })
    return Response(data, status=http_status, mimetype="application/json")


if __name__ == "__main__":
    args = docopt(__doc__)
    port = int(args["--port"])
    if args["--debug"]:
        app.debug = True
    app.config[STATUS_KEY] = int(args["<status>"])
    app.run(port=port)

