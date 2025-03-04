from flask import Blueprint, request, redirect, url_for, make_response, render_template, session
from flask_babel import gettext as _

main = Blueprint('main', __name__)

@main.route('/menu')
def menu():
    return render_template('main/menu.html')

@main.route('/set_language/<lang_code>')
def set_language(lang_code):
    supported = ["de", "en", "fr"]
    if lang_code not in supported:
        lang_code = "de"
    session['lang'] = lang_code  # Sprache in der Session speichern
    return redirect(request.referrer or url_for('main.menu'))



