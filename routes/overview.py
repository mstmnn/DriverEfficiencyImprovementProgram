from flask import Blueprint, render_template
from flask_babel import _

overview_bp = Blueprint('overview', __name__, template_folder='../templates/overview')

@overview_bp.route('/')
def overview():
    # Hier kannst du später die Logik für die Overview-Seite einfügen.
    return render_template('overview.html', title=_("Overview"))
