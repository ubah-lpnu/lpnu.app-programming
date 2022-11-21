from flask import Flask
# from pages.user import user
# from pages.note import note
from to_test.pages.tag import tag
from to_test.pages.user import user
from to_test.pages.note import note
from blueprint import api_blueprint
from flask_jwt_extended import (
    JWTManager
)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)



app.register_blueprint(tag)
app.register_blueprint(user)
app.register_blueprint(note)
app.register_blueprint(api_blueprint)


if __name__ == "__main__":
    app.run(debug=True)

# curl -v -XGET http://localhost:5000/api/v1/hello-world