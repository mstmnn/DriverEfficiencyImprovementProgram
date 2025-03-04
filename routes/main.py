from flask import Blueprint, render_template
from flask_babel import _

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

@main_bp.route('/')
def index():
    greeting = _("Hello, World!")
    return render_template('index.html', greeting=greeting)
