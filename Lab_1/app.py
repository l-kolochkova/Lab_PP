from flask import Flask, render_template
from gevent.pywsgi import WSGIServer
from sqlalchemy import create_engine
from data_base import app
# from data_base import User
from data_base import manager

# app = Flask(__name__)

if __name__ == "__main__":
    import sys

    #manager.run()
    # app.debug = True
    # http_server = WSGIServer(('127.0.0.1', 8080), app)
    # http_server.serve_forever()

#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
#
# @app.route("/api/v1/hello-world-/<int:num_of_variant>")
# def hello_world_2(num_of_variant):
#     return render_template('index.html', value=num_of_variant)
#
#
# http_server = WSGIServer(('127.0.0.1', 8080), app)
# http_server.serve_forever()
#
