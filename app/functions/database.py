# app/functions/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Definiere den Pfad zur SQLite-Datenbank; passe ihn ggf. an
DATABASE_URL = "sqlite:///{}".format(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database.db"))

# Erstelle den Engine; bei SQLite muss 'check_same_thread' auf False gesetzt werden
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)

# Erstelle einen Sessionmaker und ein scoped_session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Deklarative Basis
Base = declarative_base()

# Eine globale Session, die du in anderen Modulen verwenden kannst:
session = SessionLocal()

def init_db():
    """
    Initialisiert die Datenbank: Erstellt alle Tabellen, die in den Modellen definiert sind.
    Stelle sicher, dass du in deinen Modellen die Basisklasse 'Base' aus diesem Modul importierst.
    """
    # Erstelle alle Tabellen, falls sie noch nicht existieren
    Base.metadata.create_all(bind=engine)
