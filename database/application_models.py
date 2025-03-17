# database/application_models.py
from database import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<UserRole {self.role_name}>'

    @staticmethod
    def create_default_roles():
        roles = ['Admin', 'Manager', 'Driver']
        for role in roles:
            if not UserRole.query.filter_by(role_name=role).first():
                new_role = UserRole(role_name=role)
                db.session.add(new_role)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(50))
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    password = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    user_role = db.relationship('UserRole', backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_role(self):
        return self.user_role.role_name

    def __repr__(self):
        return f'<User {self.username}>'
