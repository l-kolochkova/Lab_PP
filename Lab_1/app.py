from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route("/api/v1/hello-world-/<int:num_of_variant>")
def hello_world_2(num_of_variant):
    return render_template('index.html', value=num_of_variant)


http_server = WSGIServer(('127.0.0.1', 5000), app)
http_server.serve_forever()
