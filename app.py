import flask
from flask import Blueprint, send_from_directory
from restplus import api
from endpoints.test import ns as test_namespace
from endpoints.document import ns as document_namespace
import logging
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config["DEBUG"] = True

cors = CORS(app, resources={r"/tempFiles": {"origins": "http://localhost:5000"}})

logging.basicConfig(level=logging.DEBUG)


@app.route('/tempFiles/<path:path>')
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def send_static(path):
    return send_from_directory('tempFiles', path)


def init_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(test_namespace)
    api.add_namespace(document_namespace)
    flask_app.register_blueprint(blueprint)


def main():
    init_app(app)
    app.run()


if __name__ == "__main__":
    main()
