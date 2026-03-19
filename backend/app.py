import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, send_from_directory
from flask_cors import CORS
from backend.database.db import init_db
from backend.routes.service_routes import service_bp
from backend.routes.proposal_routes import proposal_bp
from backend.routes.configuration_routes import configuration_bp
from backend.routes.client_routes import client_bp
from backend.config import DEBUG, HOST, PORT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(FRONTEND_DIR),
        static_url_path='/static'
    )
    CORS(app)

    app.register_blueprint(service_bp, url_prefix='/api')
    app.register_blueprint(proposal_bp, url_prefix='/api')
    app.register_blueprint(configuration_bp, url_prefix='/api')
    app.register_blueprint(client_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return send_from_directory(os.path.join(FRONTEND_DIR, 'pages'), 'propostas.html')

    @app.route('/pages/<path:filename>')
    def pages(filename):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'pages'), filename)

    @app.route('/css/<path:filename>')
    def css(filename):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'css'), filename)

    @app.route('/js/<path:filename>')
    def js(filename):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'js'), filename)

    @app.route('/components/<path:filename>')
    def components(filename):
        return send_from_directory(os.path.join(FRONTEND_DIR, 'components'), filename)

    return app


if __name__ == '__main__':
    init_db()
    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)
