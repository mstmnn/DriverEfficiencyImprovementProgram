from flask import Flask, render_template, Blueprint, request
from flask_babel import Babel, _

app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

babel = Babel(app)

# Sprachwahl: Über URL-Parameter z.B. ?lang=de
@babel.localeselector
def get_locale():
    return request.args.get('lang') or 'en'

# Blueprint definieren
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Übersetzbare Texte
    greeting = _("Hello, World!")
    return render_template('index.html', greeting=greeting)

# Blueprint registrieren
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)
