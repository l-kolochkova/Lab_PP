
from gevent.pywsgi import WSGIServer

from data_base import aplication


aplication.debug = True
http_server = WSGIServer(('127.0.0.1', 5000), aplication)
http_server.serve_forever()
# coverage run --omit 'venv/*' -m pytest -q test_flask.py
# coverage report --omit 'venv/*' -m
