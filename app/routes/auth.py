# app/routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User  # Passe den Importpfad ggf. an
from app.functions.database import db  # Dein SQLAlchemy-Objekt

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Einfache Validierung
        if not username or not password or not confirm_password:
            flash("Bitte alle Felder ausfüllen.", "error")
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash("Passwörter stimmen nicht überein.", "error")
            return redirect(url_for('auth.register'))
        
        # Überprüfen, ob der Benutzer bereits existiert
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Benutzername existiert bereits.", "error")
            return redirect(url_for('auth.register'))
        
        # Neuen Benutzer erstellen und Passwort hashen
        new_user = User(
            username=username,
            password=generate_password_hash(password, method='sha256')
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registrierung erfolgreich. Bitte melde dich an.", "success")
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Ein Fehler ist aufgetreten: {e}", "error")
            return redirect(url_for('auth.register'))
    
    # GET-Anfrage – Registrierungsformular anzeigen
    return render_template('auth/register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    # Einfaches Beispiel für Login (weitere Validierung und Session-Handling nötig)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            flash("Ungültige Anmeldedaten.", "error")
            return redirect(url_for('auth.login'))
        
        # Hier wird die Anmeldung durchgeführt – z. B. über Flask-Login (nicht vollständig implementiert)
        flash("Erfolgreich angemeldet.", "success")
        return redirect(url_for('main.menu'))
    
    return render_template('auth/login.html')
