# database/drivers_score_arch_models.py
from sqlalchemy import Table, Column, Integer, Numeric, MetaData
from database import db

def create_driver_score_arch_table(app, driver_id, bind_key='drivers_score_arch'):
    table_name = f"score_arch_{driver_id}"
    engine = db.get_engine(app, bind=bind_key)
    metadata = MetaData(bind=engine)
    
    driver_score_arch_table = Table(
        table_name, metadata,
        Column('id', Integer, primary_key=True),
        Column('user_score', Numeric(10, 2)),
        # Weitere Spalten können hier ergänzt werden
    )
    driver_score_arch_table.create(engine, checkfirst=True)
    return driver_score_arch_table
