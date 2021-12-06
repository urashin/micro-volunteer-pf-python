# python3.9

from flask import Flask

from Web.LineMessaging import LineMessaging
from Web.Api import Api
import config

app = Flask(__name__)


@app.route("/hello")
def hello():
    return {"message": "hello World"}


LineMessaging(app)
Api(app)


if __name__ == "__main__":
    app.run(
        host=config.http_host,
        port=config.http_port,
        debug=True,
    )
