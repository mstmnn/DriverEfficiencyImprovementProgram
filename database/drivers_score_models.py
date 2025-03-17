# database/drivers_score_models.py
from sqlalchemy import Table, Column, Integer, Numeric, MetaData
from database import db

def create_driver_score_table(app, driver_id, bind_key='drivers_score'):
    table_name = f"current_score_{driver_id}"
    engine = db.get_engine(app, bind=bind_key)
    metadata = MetaData(bind=engine)
    
    driver_score_table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('user_score', Numeric(10, 2)),
        # Hier können weitere Spalten ergänzt werden
    )
    driver_score_table.create(engine, checkfirst=True)
    return driver_score_table
