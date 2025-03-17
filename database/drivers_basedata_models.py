# database/drivers_basedata_models.py
from database import db
from sqlalchemy import func

class TripBaseData(db.Model):
    __tablename__ = 'trip_base_data'
    __bind_key__ = 'drivers_base_data'
    
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(255))
    # Hier wird der ForeignKey entfernt, da die Tabelle "user" in einer anderen Datenbank liegt
    driver_id = db.Column(db.Integer, nullable=False)
    drive_duration_seconds = db.Column(db.Integer)
    driving_time_seconds = db.Column(db.Integer)
    eco_distance_km = db.Column(db.Numeric(10,2))
    total_fuel_consumption_l = db.Column(db.Numeric(10,2))
    avg_fuel_consumption_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_km_per_l = db.Column(db.Numeric(5,2))
    avg_co2_emission_kg_per_100km = db.Column(db.Numeric(6,2))
    gear_shifting_overview = db.Column(db.String(255))
    avg_axle_load_t = db.Column(db.Numeric(5,2))
    avg_rpm = db.Column(db.Integer)
    avg_speed_km_per_h = db.Column(db.Numeric(5,2))
    total_fuel_consumption_driving_l = db.Column(db.Numeric(10,2))
    avg_fuel_consumption_driving_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_driving_km_per_l = db.Column(db.Numeric(5,2))
    idle_time_seconds = db.Column(db.Integer)
    idle_time_percentage = db.Column(db.Numeric(5,2))
    idle_fuel_l = db.Column(db.Numeric(10,2))
    idle_time_pto_seconds = db.Column(db.Integer)
    idle_time_pto_percentage = db.Column(db.Numeric(5,2))
    idle_fuel_pto_l = db.Column(db.Numeric(10,2))
    number_of_long_idle = db.Column(db.Integer)
    long_idle_events = db.Column(db.Integer)
    time_over_max_speed_seconds = db.Column(db.Integer)
    time_over_max_speed_percentage = db.Column(db.Numeric(5,2))
    coasting_time_seconds = db.Column(db.Integer)
    coasting_distance_km = db.Column(db.Numeric(10,2))
    coasting_distance_percentage = db.Column(db.Numeric(5,2))
    cruise_control_time_seconds = db.Column(db.Integer)
    cruise_control_distance_km = db.Column(db.Numeric(10,2))
    cruise_control_distance_percentage = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_cruise_l_per_100km = db.Column(db.Numeric(5,2))
    avg_fuel_consumption_cruise_km_per_l = db.Column(db.Numeric(5,2))
    braking_time_seconds = db.Column(db.Integer)
    braking_distance_m = db.Column(db.Integer)
    braking_distance_percentage = db.Column(db.Numeric(5,2))
    number_of_brakings = db.Column(db.Integer)
    brakings_per_100km = db.Column(db.Numeric(5,2))
    high_rpm_no_fuel_seconds = db.Column(db.Integer)
    retarder_active_seconds = db.Column(db.Integer)
    retarder_active_percentage = db.Column(db.Numeric(5,2))
    number_of_stops = db.Column(db.Integer)
    stops_per_100km = db.Column(db.Numeric(5,2))
    number_of_panic_brakings = db.Column(db.Integer)
    panic_brakings_per_100km = db.Column(db.Numeric(5,2))
    green_zone_distance_km = db.Column(db.Numeric(10,2))
    avg_throttle_position_percentage = db.Column(db.Numeric(5,2))
    rpm_at_top_speed = db.Column(db.Integer)
    # Weitere Felder ...
    created_at = db.Column(db.DateTime, server_default=func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f'<TripBaseData {self.id} (vehicle={self.vehicle}, driver={self.driver_id})>'
