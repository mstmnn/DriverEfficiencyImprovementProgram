from flask import Flask
from flask_babel import Babel
from models.models import db
from routes.auth import auth_bp
from routes.main import main_bp
from routes.datamodel import datamodel_bp
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dein-geheimer-schluessel'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'models', 'app.db')
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

# Datenbank initialisieren
db.init_app(app)

# Sprachwechsler-Funktion
def get_locale():
    from flask import request
    return request.args.get('lang') or 'en'

# Babel initialisieren und get_locale im Jinja-Kontext registrieren
babel = Babel(app, locale_selector=get_locale)
app.jinja_env.globals['get_locale'] = get_locale

# Blueprints registrieren
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(datamodel_bp)

# Datenbanktabellen erstellen (im App-Kontext)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
