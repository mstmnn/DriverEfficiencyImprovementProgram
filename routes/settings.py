from flask import Blueprint, render_template
from flask_babel import _

settings_bp = Blueprint('settings', __name__, template_folder='../templates/settings')

@settings_bp.route('/')
def settings():
    # Hier kannst du später die Logik für die Settings-Seite einfügen.
    return render_template('settings.html', title=_("Settings"))
