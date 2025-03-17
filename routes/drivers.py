from flask import Blueprint, render_template, current_app
from flask_babel import _
from database.application_models import User, Result  # Result wird hier angenommen als Beziehung zu User
from database import db
from sqlalchemy import Table, MetaData, select

drivers_bp = Blueprint('drivers', __name__, template_folder='../templates/drivers')

def get_archived_scores(driver_id):
    """
    Diese Funktion lädt dynamisch die archivierte Score-Tabelle für den Fahrer
    und gibt alle Einträge als Liste von Dictionaries zurück.
    """
    bind_key = 'drivers_score_arch'
    engine = db.get_engine(current_app, bind=bind_key)
    metadata = MetaData(bind=engine)
    table_name = f"score_arch_{driver_id}"
    
    try:
        # Versuche, die existierende Tabelle dynamisch zu laden
        archived_table = Table(table_name, metadata, autoload_with=engine)
    except Exception as e:
        # Falls die Tabelle nicht existiert, wird eine leere Liste zurückgegeben.
        current_app.logger.error(f"Table {table_name} not found: {e}")
        return []
    
    stmt = select(archived_table)
    with engine.connect() as conn:
        result_proxy = conn.execute(stmt)
        rows = result_proxy.fetchall()
    
    scores = []
    for row in rows:
        scores.append({
            'id': row['id'],
            'score': float(row['user_score'])
        })
    return scores

@drivers_bp.route('/')
def overview():
    """
    Übersicht aller Fahrer:
    - Ruft alle User ab, bei denen role_id == 4 ist.
    - Ermittelt für jeden Fahrer den aktuellen Score aus der Results-Tabelle (angenommene Beziehung).
    - Übergibt die Daten an das Template, um sie in einem responsiven Grid (z. B. in 5 Spalten) anzuzeigen.
    """
    # Abrufen aller Fahrer mit role_id == 4
    drivers = User.query.filter_by(role_id=4).all()
    driver_data = []
    for driver in drivers:
        # Versuche, den aktuellsten Score zu ermitteln – hier wird angenommen, dass
        # die Beziehung "results" vorhanden ist und Ergebnisse sortiert werden können.
        if hasattr(driver, 'results') and driver.results:
            # Sortierung anhand der ID (oder eines Zeitstempels, falls vorhanden)
            latest_result = sorted(driver.results, key=lambda r: r.id)[-1]
            current_score = latest_result.user_score
        else:
            current_score = None
        driver_data.append({
            'id': driver.id,
            'username': driver.username,
            'current_score': current_score
        })
    return render_template('drivers_overview.html', title=_("Drivers Overview"), drivers=driver_data)

@drivers_bp.route('/<int:driver_id>')
def driver_detail(driver_id):
    """
    Detailansicht eines Fahrers:
    - Zeigt detaillierte Informationen wie E-Mail, Telefonnummer, Benutzername.
    - Ruft über die Funktion get_archived_scores() die archivierten Scores für diesen Fahrer ab.
    """
    driver = User.query.filter_by(id=driver_id, role_id=4).first_or_404()
    archived_scores = get_archived_scores(driver_id)
    return render_template('driver_detail.html', title=_("Driver Detail"), driver=driver, archived_scores=archived_scores)

@drivers_bp.route('/archive')
def archive_overview():
    """
    Archiv-Übersicht:
    - Zeigt für alle Fahrer (role_id == 4) eine Zusammenfassung der archivierten Scores.
    """
    drivers = User.query.filter_by(role_id=4).all()
    archive_data = []
    for driver in drivers:
        archived_scores = get_archived_scores(driver.id)
        archive_data.append({
            'id': driver.id,
            'username': driver.username,
            'archived_scores': archived_scores
        })
    return render_template('drivers_archive.html', title=_("Drivers Archive"), archive_data=archive_data)
