from flask import Flask
from flask_babel import Babel
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from database import db, init_db
from database.application_models import User, UserRole
from database.drivers_basedata_models import TripBaseData
from database.drivers_score_models import create_driver_score_table
from database.drivers_score_arch_models import create_driver_score_arch_table
from database.drivers_basedata_arch_models import TripBaseDataArch

app = Flask(__name__)
app.config.from_object(Config)

# Extensions initialisieren
init_db(app)
mail = Mail(app)

def get_locale():
    from flask import request
    return request.args.get('lang') or app.config['BABEL_DEFAULT_LOCALE']

# Babel wird mit dem locale_selector-Parameter initialisiert
babel = Babel(app, locale_selector=get_locale)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Beispiel: falls nicht eingeloggt, zur Login-Seite

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.jinja_env.globals['get_locale'] = get_locale

from routes.auth import auth_bp
from routes.main import main_bp
from routes.overview import overview_bp
from routes.settings import settings_bp
from routes.datamodel import datamodel_bp
from routes.drivers import drivers_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(overview_bp, url_prefix='/overview')
app.register_blueprint(settings_bp, url_prefix='/settings')
app.register_blueprint(datamodel_bp)
app.register_blueprint(drivers_bp)

if __name__ == '__main__':
    app.run(debug=True)
