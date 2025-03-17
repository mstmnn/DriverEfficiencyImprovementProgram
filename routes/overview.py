from flask import Blueprint, render_template
from flask_babel import _
from flask_login import login_required

overview_bp = Blueprint('overview', __name__, template_folder='../templates/overview')

@overview_bp.route('/')
@login_required
def overview():
    return render_template('current_month.html', title=_("Overview"))

@overview_bp.route('/arch')
@login_required
def overview_archive():
    return render_template('overview_archive.html', title=_("Overview"))
