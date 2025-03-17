from flask import Blueprint, render_template
from flask_babel import _
from database.application_models import User

datamodel_bp = Blueprint('datamodel', __name__, url_prefix='/data', template_folder='../templates/datamodel')

@datamodel_bp.route('/users')
def list_users():
    users = User.query.all()
    return render_template('users.html', users=users)
