# app.py oder deine Hauptanwendung
import os
from flask import Flask
from flask_babel import Babel
from database.database import init_db, db
from routes.auth import auth_bp, mail  # Importiere hier auch das Mail-Objekt
from routes.main import main_bp
from routes.overview import overview_bp
from routes.settings import settings_bp
from routes.datamodel import datamodel_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dein-geheimer-schluessel'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:BL2mIRdabe!@localhost/driver_performance'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'
    
    # Konfiguration für Flask-Mail – bitte an deine Mail-Provider-Daten anpassen!
    app.config['MAIL_SERVER'] = 'postbox.luxport.lu'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'max.steinmann@luxport-group.com'
    app.config['MAIL_PASSWORD'] = 'LuxportSA2021$'
    app.config['MAIL_DEFAULT_SENDER'] = 'max.steinmann@luxport-group.com'

    init_db(app)
    
    with app.app_context():
        db.create_all()

    # Initialisiere Flask-Mail
    mail.init_app(app)
    
    # Sprachwechsler-Funktion
    def get_locale():
        from flask import request
        return request.args.get('lang') or 'en'
    
    babel = Babel(app, locale_selector=get_locale)
    app.jinja_env.globals['get_locale'] = get_locale

    # Blueprints registrieren
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(overview_bp, url_prefix='/overview')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(datamodel_bp)

    return app
 
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
