from database.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func


class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<UserRole {self.role_name}>'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(50))
    role = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    password = db.Column(db.String(255), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)  # Neues Feld für Email-Bestätigung

    user_role = db.relationship('UserRole', backref=db.backref('users', lazy=True))
    results = db.relationship('Result', backref='user', lazy=True)
    trips = db.relationship('TripBaseData', backref='driver', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_score = db.Column(db.Numeric(10, 2))

    def __repr__(self):
        return f'<Result {self.id} for User {self.user_id}>'

class TripBaseData(db.Model):
    __tablename__ = 'trip_base_data'
    id = db.Column(db.Integer, primary_key=True)
    
    # Optional: Fahrzeugbezeichnung
    vehicle = db.Column(db.String(255))
    
    # Verknüpfung zum Benutzer (Fahrer)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Fahrtdauer
    drive_duration_hms = db.Column(db.Time)        # Fahrtdauer (HH:MM:SS)
    drive_duration_seconds = db.Column(db.Integer) # Fahrtdauer (s)
    
    # Fahrzeit
    driving_time_hms = db.Column(db.Time)          # Fahrzeit (HH:MM:SS)
    driving_time_seconds = db.Column(db.Integer)   # Fahrzeit (s)
    
    # ECO-Strecke und Kraftstoff
    eco_distance_km = db.Column(db.Numeric(10,2))
    total_fuel_consumption_l = db.Column(db.Numeric(10,2))
    avg_fuel_consumption_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_km_per_l = db.Column(db.Numeric(5,2))
    
    # CO2
    avg_co2_emission_kg_per_100km = db.Column(db.Numeric(6,2))
    
    # Übersicht des Schaltverhaltens (falls gewünscht)
    gear_shifting_overview = db.Column(db.String(255))
    
    # Achslast, Drehzahl, Geschwindigkeit
    avg_axle_load_t = db.Column(db.Numeric(5,2))
    avg_rpm = db.Column(db.Integer)  # Durchschnittliche Drehzahl
    avg_speed_km_per_h = db.Column(db.Numeric(5,2))
    
    # Kraftstoff nur beim Fahren
    total_fuel_consumption_driving_l = db.Column(db.Numeric(10,2))
    avg_fuel_consumption_driving_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_driving_km_per_l = db.Column(db.Numeric(5,2))
    
    # Leerlauf
    idle_time_hms = db.Column(db.Time)             # Standzeit im Leerlauf (HH:MM:SS)
    idle_time_seconds = db.Column(db.Integer)      # Standzeit im Leerlauf (s)
    idle_time_percentage = db.Column(db.Numeric(5,2))
    idle_fuel_l = db.Column(db.Numeric(10,2))
    
    # Leerlauf + PTO
    idle_time_pto_hms = db.Column(db.Time)
    idle_time_pto_seconds = db.Column(db.Integer)
    idle_time_pto_percentage = db.Column(db.Numeric(5,2))
    idle_fuel_pto_l = db.Column(db.Numeric(10,2))
    
    # Leerlauf > Maximalgeschwindigkeit
    idle_over_max_speed_count = db.Column(db.Integer)
    
    # Längeres Laufenlassen
    number_of_long_idle = db.Column(db.Integer)
    long_idle_events = db.Column(db.Integer)
    
    # Fahrzeit über Maximalgeschwindigkeit
    time_over_max_speed_hms = db.Column(db.Time)
    time_over_max_speed_seconds = db.Column(db.Integer)
    time_over_max_speed_percentage = db.Column(db.Numeric(5,2))
    speed_over_max_count = db.Column(db.Integer)  # Geschwindigkeit > Maximalgeschwindigkeit (#)
    
    # Schubbetrieb
    coasting_time_hms = db.Column(db.Time)
    coasting_time_seconds = db.Column(db.Integer)
    coasting_distance_km = db.Column(db.Numeric(10,2))
    coasting_distance_percentage = db.Column(db.Numeric(5,2))
    
    # Tempomat
    cruise_control_time_hms = db.Column(db.Time)
    cruise_control_time_seconds = db.Column(db.Integer)
    cruise_control_distance_km = db.Column(db.Numeric(10,2))
    cruise_control_distance_percentage = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_cruise_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_cruise_km_per_l = db.Column(db.Numeric(5,2))
    
    # Bremsen
    braking_time_hms = db.Column(db.Time)
    braking_time_seconds = db.Column(db.Integer)
    braking_distance_m = db.Column(db.Integer)
    braking_distance_percentage = db.Column(db.Numeric(5,2))
    number_of_brakings = db.Column(db.Integer)
    brakings_per_100km = db.Column(db.Numeric(5,2))
    
    # Hohe Drehzahl ohne Kraftstoff
    high_rpm_no_fuel_time_hms = db.Column(db.Time)
    high_rpm_no_fuel_seconds = db.Column(db.Integer)
    
    # Retarder
    retarder_active_time_hms = db.Column(db.Time)
    retarder_active_seconds = db.Column(db.Integer)
    retarder_active_percentage = db.Column(db.Numeric(5,2))
    
    # Stopps
    number_of_stops = db.Column(db.Integer)
    stops_per_100km = db.Column(db.Numeric(5,2))
    
    # Panikbremsungen
    number_of_panic_brakings = db.Column(db.Integer)
    panic_brakings_per_100km = db.Column(db.Numeric(5,2))
    
    # Schaltvorgänge
    gear_shifts_count = db.Column(db.Integer)
    gear_shifts_per_100km = db.Column(db.Numeric(5,2))
    gear_shifts_up_count = db.Column(db.Integer)
    gear_shifts_up_green_count = db.Column(db.Integer)
    gear_shifts_up_green_percentage = db.Column(db.Numeric(5,2))
    gear_shifts_down_count = db.Column(db.Integer)
    gear_shifts_down_green_count = db.Column(db.Integer)
    gear_shifts_down_green_percentage = db.Column(db.Numeric(5,2))
    
    # Grüne Zone
    green_zone_distance_km = db.Column(db.Numeric(10,2))
    green_zone_distance_percentage = db.Column(db.Numeric(5,2))
    
    # Gaspedal
    avg_throttle_position_percentage = db.Column(db.Numeric(5,2))
    max_throttle_position_percentage = db.Column(db.Numeric(5,2))
    
    # Drehzahl Höchstgeschwindigkeit
    rpm_at_top_speed = db.Column(db.Integer)
    
    # Dauer je Gang (s)
    gear_1_time_seconds = db.Column(db.Integer)
    gear_2_time_seconds = db.Column(db.Integer)
    gear_3_time_seconds = db.Column(db.Integer)
    gear_4_time_seconds = db.Column(db.Integer)
    gear_5_time_seconds = db.Column(db.Integer)
    gear_6_time_seconds = db.Column(db.Integer)
    gear_7_time_seconds = db.Column(db.Integer)
    gear_8_time_seconds = db.Column(db.Integer)
    gear_9_time_seconds = db.Column(db.Integer)
    gear_10_time_seconds = db.Column(db.Integer)
    gear_11_time_seconds = db.Column(db.Integer)
    gear_12_time_seconds = db.Column(db.Integer)
    gear_13_time_seconds = db.Column(db.Integer)
    gear_14_time_seconds = db.Column(db.Integer)
    gear_15_time_seconds = db.Column(db.Integer)
    gear_16_time_seconds = db.Column(db.Integer)
    
    # PTO-Zeit
    pto_time_standstill_hms = db.Column(db.Time)
    pto_time_standstill_seconds = db.Column(db.Integer)
    pto_time_driving_hms = db.Column(db.Time)
    pto_time_driving_seconds = db.Column(db.Integer)
    pto_fuel_standstill_l = db.Column(db.Numeric(10,2))
    pto_fuel_standstill_l_per_h = db.Column(db.Numeric(5,2))
    pto_count = db.Column(db.Integer)
    
    # Zeitstempel
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<TripBaseData {self.id} (vehicle={self.vehicle}, driver={self.driver_id})>'