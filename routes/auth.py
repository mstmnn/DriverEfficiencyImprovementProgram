from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_babel import _
from models.models import db, User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            flash(_('Logged in successfully.'), 'success')
            # Hier könntest du eine Session setzen (z. B. mit Flask-Login)
            return redirect(url_for('main.index'))
        else:
            flash(_('Invalid username or password.'), 'danger')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if User.query.filter_by(username=username).first():
            flash(_('Username already exists.'), 'danger')
            return redirect(url_for('auth.register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash(_('Registration successful. Please login.'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
