# config.py
class Config:
    SECRET_KEY = 'dein-geheimer-schluessel'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:BL2mIRdabe!@localhost/applicationdata'
    SQLALCHEMY_BINDS = {
        'drivers_score': 'mysql+pymysql://root:BL2mIRdabe!@localhost/driversscore',
        'drivers_score_arch': 'mysql+pymysql://root:BL2mIRdabe!@localhost/driversscorearch',
        'drivers_base_data': 'mysql+pymysql://root:BL2mIRdabe!@localhost/driversbasedata',
        'drivers_base_data_arch': 'mysql+pymysql://root:BL2mIRdabe!@localhost/driversbasedataarch'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_TRANSLATION_DIRECTORIES = 'translations'
    MAIL_SERVER = 'postbox.luxport.lu'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'noreply.luxport'
    MAIL_PASSWORD = 'Sup3rMar!o'
    MAIL_DEFAULT_SENDER = 'noreply@luxport-group.com'
