# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_babel import _
from database.models import db, User
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail

# Mail-Objekt, das in create_app() initialisiert wird
mail = Mail()

# Nutze denselben geheimen Schlüssel wie in der App-Konfiguration
serializer = URLSafeTimedSerializer('dein-geheimer-schluessel')

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = email.split('@')[0]
        if User.query.filter_by(username=username).first():
            flash(_('Username already exists.'), 'danger')
            return redirect(url_for('auth.register'))
        if User.query.filter_by(email=email).first():
            flash(_('Email already exists.'), 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = User(username=username, email=email, confirmed=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        # Generiere einen Bestätigungstoken
        token = serializer.dumps(email, salt='email-confirm-salt')
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        html = render_template('activate.html', confirm_url=confirm_url)
        subject = _('Please confirm your email')
        # Verwende current_app, um auf die Konfiguration zuzugreifen:
        msg = Message(subject, 
                      sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'your_email@example.com'),
                      recipients=[email], html=html)
        mail.send(msg)
        
        flash(_('Registration successful. Please check your email to confirm your account.'), 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=3600)
    except Exception:
        flash(_('The confirmation link is invalid or has expired.'), 'danger')
        return redirect(url_for('auth.login'))
    
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash(_('Account already confirmed. Please login.'), 'success')
    else:
        user.confirmed = True
        db.session.commit()
        flash(_('You have confirmed your account. Thank you!'), 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_input = request.form.get('login')
        password = request.form.get('password')
        if '@' in login_input:
            user = User.query.filter_by(email=login_input).first()
        else:
            user = User.query.filter_by(username=login_input).first()
        if user and user.check_password(password):
            if not user.confirmed:
                flash(_('Please confirm your email address before logging in.'), 'warning')
                return redirect(url_for('auth.login'))
            flash(_('Logged in successfully.'), 'success')
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            flash(_('Invalid username/email or password.'), 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash(_('You have been logged out.'), 'success')
    return redirect(url_for('auth.login'))
