import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash, current_app
from flask_babel import _
from flask_login import login_required
from werkzeug.utils import secure_filename
from database.drivers_basedata_models import db, TripBaseData

main_bp = Blueprint('main', __name__, template_folder='../templates/main')

# Erlaubte Dateiendungen für Excel-Dateien
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/')
@login_required
def index():
    greeting = _("Hello, World!")
    return render_template('index.html', greeting=greeting)

@main_bp.route('/upload-file')
@login_required
def upload_file():
    return render_template('main/upload_file.html', title=_("Upload File"))

@main_bp.route('/upload-file-handler', methods=['POST'])
@login_required
def upload_file_handler():
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
        
        try:
            df = pd.read_excel(filepath)
        except Exception as e:
            return jsonify({'error': _("Error reading Excel file: ") + str(e)}), 500
        
        inserted = 0
        for index, row in df.iterrows():
            # Beispiel: Eindeutigkeit anhand driver_id und drive_duration_seconds
            existing = TripBaseData.query.filter_by(
                driver_id=row['driver_id'],
                drive_duration_seconds=row['drive_duration_seconds']
            ).first()
            
            if not existing:
                new_record = TripBaseData(
                    driver_id = row['driver_id'],
                    drive_duration_seconds = row['drive_duration_seconds'],
                    driving_time_seconds = row['driving_time_seconds'],
                    eco_distance_km = row['eco_distance_km'],
                    total_fuel_consumption_l = row['total_fuel_consumption_l'],
                    avg_fuel_consumption_l_per_100km = row['avg_fuel_consumption_l_per_100km'],
                    avg_fuel_consumption_km_per_l = row['avg_fuel_consumption_km_per_l'],
                    avg_axle_load_t = row['avg_axle_load_t'],
                    avg_speed_km_per_h = row['avg_speed_km_per_h'],
                    total_fuel_consumption_driving_l = row['total_fuel_consumption_driving_l'],
                    avg_fuel_consumption_driving_l_per_100km = row['avg_fuel_consumption_driving_l_per_100km'],
                    avg_fuel_consumption_driving_km_per_l = row['avg_fuel_consumption_driving_km_per_l'],
                    idle_time_seconds = row['idle_time_seconds'],
                    idle_time_percentage = row['idle_time_percentage'],
                    idle_fuel_l = row['idle_fuel_l'],
                    idle_time_pto_seconds = row['idle_time_pto_seconds'],
                    idle_time_pto_percentage = row['idle_time_pto_percentage'],
                    idle_fuel_pto_l = row['idle_fuel_pto_l'],
                    number_of_long_idle = row['number_of_long_idle'],
                    long_idle_events = row['long_idle_events'],
                    time_over_max_speed_seconds = row['time_over_max_speed_seconds'],
                    time_over_max_speed_percentage = row['time_over_max_speed_percentage'],
                    coasting_time_seconds = row['coasting_time_seconds'],
                    coasting_distance_km = row['coasting_distance_km'],
                    coasting_distance_percentage = row['coasting_distance_percentage'],
                    cruise_control_time_seconds = row['cruise_control_time_seconds'],
                    cruise_control_distance_km = row['cruise_control_distance_km'],
                    cruise_control_distance_percentage = row['cruise_control_distance_percentage'],
                    avg_fuel_consumption_cruise_l_per_100km = row['avg_fuel_consumption_cruise_l_per_100km'],
                    avg_fuel_consumption_cruise_km_per_l = row['avg_fuel_consumption_cruise_km_per_l'],
                    braking_time_seconds = row['braking_time_seconds'],
                    braking_distance_m = row['braking_distance_m'],
                    braking_distance_percentage = row['braking_distance_percentage'],
                    number_of_brakings = row['number_of_brakings'],
                    brakings_per_100km = row['brakings_per_100km'],
                    high_rpm_no_fuel_seconds = row['high_rpm_no_fuel_seconds'],
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
