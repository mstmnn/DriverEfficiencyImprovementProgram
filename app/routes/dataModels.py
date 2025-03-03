# app/routes/dataModels.py
from flask import Blueprint, render_template, request, redirect, url_for, flash

dataModels = Blueprint('dataModels', __name__)

@dataModels.route('/', methods=['GET'])
def list_models():
    # Hier Modelle aus der Datenbank abrufen (Beispiel: leere Liste)
    models = []
    return render_template('dataModels/list.html', models=models)

@dataModels.route('/edit/<int:model_id>', methods=['GET', 'POST'])
def edit_model(model_id):
    if request.method == 'POST':
        # Update-Logik hier einfügen
        return redirect(url_for('dataModels.list_models'))
    # Hier ein einzelnes Modell laden (Beispiel: leeres Dict)
    model = {}
    return render_template('dataModels/edit.html', model=model)
