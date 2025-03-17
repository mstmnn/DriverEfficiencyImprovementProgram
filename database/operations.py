from . import db
from .application_models import User, UserRole


def create_user(username, email, password):
    # Setze die Rolle standardmäßig auf 'Driver'
    role = UserRole.query.filter_by(role_name='Driver').first()
    
    new_user = User(username=username, email=email, password=password, role_id=role.id)
    db.session.add(new_user)
    db.session.commit()


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

