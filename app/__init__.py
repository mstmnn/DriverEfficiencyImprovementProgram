import os
from flask import Flask, request, session
from flask_cors import CORS
from flask_babel import Babel, gettext, force_locale, _
from app.extensions import db  # z.B. Flask-SQLAlchemy-Objekt

def create_app():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/"))

    app.config["DEBUG"] = True
    app.config["SECRET_KEY"] = "dein_einzigartiger_geheimer_schluessel"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}".format(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Babel-Konfiguration
    app.config["BABEL_DEFAULT_LOCALE"] = "de"
    app.config["BABEL_SUPPORTED_LOCALES"] = ["de", "en", "fr"]
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "translations")


    CORS(app, resources={r"/*": {"origins": "*"}})
    db.init_app(app)

    # Blueprints importieren und registrieren
    from app.routes.auth import auth
    from app.routes.dataModels import dataModels
    from app.routes.main import main

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(dataModels, url_prefix="/dataModels")
    app.register_blueprint(main, url_prefix="/")

    with app.app_context():
        db.create_all()

    babel = Babel(app)


    def get_locale():
        lang = session.get('lang')
        print("Aktuelle Session-Sprache:", lang)  # Debug-Ausgabe
        if lang in app.config["BABEL_SUPPORTED_LOCALES"]:
            return lang
        best = request.accept_languages.best_match(app.config["BABEL_SUPPORTED_LOCALES"])
        print("Accept-Language Fallback:", best)
        return best

    babel.init_app(app, locale_selector=get_locale)
    @app.context_processor
    def inject_locale():
        print("inject_locale wurde aufgerufen!")  # Debug-Ausgabe
        return dict(get_locale=get_locale, gettext=gettext)
    
    with force_locale("fr"):
        print(gettext("Benutzername"))

    return app

app = create_app()
