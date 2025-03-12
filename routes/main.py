import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from flask_babel import _
from werkzeug.utils import secure_filename
from database.models import db, TripBaseData  # Stelle sicher, dass TripBaseData importiert wird

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

# Erlaubte Dateiendungen für Excel-Dateien
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    greeting = _("Hello, World!")
    return render_template('index.html', greeting=greeting)

@main_bp.route('/upload-file')
def upload_file():
    return render_template('main/upload_file.html', title=_("Upload File"))

@main_bp.route('/upload-file-handler', methods=['POST'])
def upload_file_handler():
    # Prüfen, ob ein File im Request vorhanden ist
    if 'file' not in request.files:
        return jsonify({'error': _("No file part")}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': _("No selected file")}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Versuche, die Excel-Datei mit pandas auszulesen
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': _("Error reading Excel file: ") + str(e)}), 500
        
        inserted = 0
        # Für jede Zeile in der Excel-Datei: Prüfen, ob die Daten bereits vorhanden sind.
        # Hier verwenden wir als Beispiel die Kombination von 'driver_id' und 'drive_duration'
        for index, row in df.iterrows():
            # Achtung: Passe den Uniqueness-Check an deine Datenstruktur an.
            existing = TripBaseData.query.filter_by(
                driver_id=row['driver_id'],
                drive_duration=row['drive_duration']
            ).first()
            
            if not existing:
                new_record = TripBaseData(
                    driver_id = row['driver_id'],
                    drive_duration = row['drive_duration'],
                    driving_time = row['driving_time'],
                    eco_distance_km = row['eco_distance_km'],
                    total_fuel_consumption_l = row['total_fuel_consumption_l'],
                    avg_fuel_consumption_l_per_100km = row['avg_fuel_consumption_l_per_100km'],
                    avg_fuel_consumption_km_per_l = row['avg_fuel_consumption_km_per_l'],
                    avg_axle_load_t = row['avg_axle_load_t'],
                    avg_speed_km_per_h = row['avg_speed_km_per_h'],
                    total_fuel_consumption_driving_l = row['total_fuel_consumption_driving_l'],
                    avg_fuel_consumption_driving_l_per_100km = row['avg_fuel_consumption_driving_l_per_100km'],
                    avg_fuel_consumption_driving_km_per_l = row['avg_fuel_consumption_driving_km_per_l'],
                    idle_time = row['idle_time'],
                    idle_time_percentage = row['idle_time_percentage'],
                    idle_fuel_l = row['idle_fuel_l'],
                    idle_time_pto = row['idle_time_pto'],
                    idle_time_pto_percentage = row['idle_time_pto_percentage'],
                    idle_fuel_pto_l = row['idle_fuel_pto_l'],
                    number_of_long_idle = row['number_of_long_idle'],
                    long_idle_events = row['long_idle_events'],
                    time_over_max_speed = row['time_over_max_speed'],
                    time_over_max_speed_percentage = row['time_over_max_speed_percentage'],
                    coasting_time = row['coasting_time'],
                    coasting_distance_km = row['coasting_distance_km'],
                    coasting_distance_percentage = row['coasting_distance_percentage'],
                    cruise_control_time = row['cruise_control_time'],
                    cruise_control_distance_km = row['cruise_control_distance_km'],
                    cruise_control_distance_percentage = row['cruise_control_distance_percentage'],
                    avg_fuel_consumption_cruise_l_per_100km = row['avg_fuel_consumption_cruise_l_per_100km'],
                    avg_fuel_consumption_cruise_km_per_l = row['avg_fuel_consumption_cruise_km_per_l'],
                    braking_time = row['braking_time'],
                    braking_time_seconds = row['braking_time_seconds'],
                    braking_distance_m = row['braking_distance_m'],
                    braking_distance_percentage = row['braking_distance_percentage'],
                    number_of_brakings = row['number_of_brakings'],
                    brakings_per_100km = row['brakings_per_100km'],
                    high_rpm_no_fuel_time = row['high_rpm_no_fuel_time'],
                    high_rpm_no_fuel_seconds = row['high_rpm_no_fuel_seconds'],
                    retarder_active_time = row['retarder_active_time'],
                    retarder_active_seconds = row['retarder_active_seconds'],
                    retarder_active_percentage = row['retarder_active_percentage'],
                    number_of_stops = row['number_of_stops'],
                    stops_per_100km = row['stops_per_100km'],
                    number_of_panic_brakings = row['number_of_panic_brakings'],
                    panic_brakings_per_100km = row['panic_brakings_per_100km'],
                    green_zone_distance_km = row['green_zone_distance_km'],
                    avg_throttle_position_percentage = row['avg_throttle_position_percentage'],
                    rpm_at_top_speed = row['rpm_at_top_speed']
                )
                db.session.add(new_record)
                inserted += 1
        
        db.session.commit()
        return jsonify({
            'success': True,
            'inserted': inserted
        }), 200
    else:
        return jsonify({'error': _("File type not allowed")}), 400
