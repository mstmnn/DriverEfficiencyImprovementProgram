# app/routes/main.py
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def menu():
    return render_template('main/menu.html')

@main.route('/report')
def report():
    return render_template('main/report.html')
