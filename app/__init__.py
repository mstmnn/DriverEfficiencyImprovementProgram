# app/__init__.py
import os
from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"))
    
    # Beispielhafte Konfiguration; passe sie nach Bedarf an
    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "dein_einzigartiger_geheimer_schluessel"
    
    # CORS aktivieren
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Blueprints importieren und registrieren
    from app.routes.auth import auth
    from app.routes.dataModels import dataModels
    from app.routes.main import main

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dataModels, url_prefix="/dataModels")
    # Für den Main-Blueprint kannst du auch das Root-Prefix verwenden:
    app.register_blueprint(main, url_prefix="/")
    
    return app

app = create_app()
