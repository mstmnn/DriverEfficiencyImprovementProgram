from flask import Blueprint, render_template
from flask_babel import _

settings_bp = Blueprint('settings', __name__, template_folder='../templates/settings')

@settings_bp.route('/')
def settings():
    return render_template('settings.html', title=_("Settings"))
