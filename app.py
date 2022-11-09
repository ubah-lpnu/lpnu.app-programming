from flask import Flask
from wsgiref.simple_server import make_server
# from pages.user import user
# from pages.note import note
from pages.tag import tag
from pages.user import user
from pages.note import note
from blueprint import api_blueprint
app = Flask(__name__)


with make_server('', 5000, app) as server:
    # app.register_blueprint(user)
    # app.register_blueprint(note)
    app.register_blueprint(tag)
    app.register_blueprint(user)
    app.register_blueprint(note)
    app.register_blueprint(api_blueprint)
    server.serve_forever()

# curl -v -XGET http://localhost:5000/api/v1/hello-world