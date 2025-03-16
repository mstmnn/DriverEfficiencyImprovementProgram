from . import db
from .models import User, UserRole


def create_user(username, email, password):
    # Setze die Rolle standardmäßig auf 'Driver'
    role = UserRole.query.filter_by(role_name='Driver').first()
    
    new_user = User(username=username, email=email, password=password, role_id=role.id)
    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('You must be logged in to access this page.', 'danger')
                return redirect(url_for('auth.login'))
            if current_user.get_role() != role_name:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('main.index'))  # Oder eine andere Route
            return func(*args, **kwargs)
        return decorated_view
    return decorator
