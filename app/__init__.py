from flask import Flask, jsonify
from flask_restx import Api
from .config.config import config_dict
from app.extensions import db, migrate, jwt
from .ressources import register_resources
import logging
from logging.handlers import RotatingFileHandler

import os

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    def setup_logging(app):
        if not os.path.exists('logs'):
            os.mkdir('logs')
        handler = RotatingFileHandler('logs/api.log', maxBytes=1024*1024, backupCount=5)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
        app.logger.setLevel(logging.INFO)

    def register_error_handlers(app):
        @app.errorhandler(401)
        def unauthorized(e):
            app.logger.warning(f"401 Unauthorized: {e}")
            return jsonify({"status": "error", "message": "Token manquant ou invalide"}), 401

    @app.errorhandler(403)
    def forbidden(e):
        app.logger.warning(f"403 Forbidden: {e}")
        return jsonify({"status": "error", "message": "Accès refusé"}), 403

    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Erreur: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

    def register_jwt_callbacks(app):
        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            app.logger.warning("Token expiré")
            return jsonify({"status": "error", "message": "Votre session a expiré, veuillez vous reconnecter."}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(msg):
        app.logger.warning(f"Token manquant: {msg}")
        return jsonify({"status": "error", "message": "Token manquant ou invalide"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(msg):
        app.logger.warning(f"Token invalide: {msg}")
        return jsonify({"status": "error", "message": "Token invalide"}), 401


    
    authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

    api = Api(app, version='1.0', title='API', description='Api Gestion de vente des produits cosmetique', authorizations=authorizations, doc="/docs")
    register_resources(api)

    return app
