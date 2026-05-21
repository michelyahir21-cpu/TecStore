from flask import Flask

from database.bd import db

from extensions import mail

from routes.auth import auth
from routes.tramites import tramites
from routes.solicitudes import solicitudes

# =========================
# APP
# =========================

app = Flask(__name__)

# =========================
# SECRET KEY
# =========================

app.secret_key = 'tecstore'

# =========================
# MYSQL
# =========================

app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'mysql+pymysql://root:1ZCGcTFyFzdHthbTNZtBHCJMdSLIzmBK@caboose.proxy.rlwy.net:16022/railway'

app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'
] = False

# =========================
# MAIL
# =========================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'

app.config['MAIL_PORT'] = 587

app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = 'tecnmstore@gmail.com'

app.config['MAIL_PASSWORD'] = 'jqvhsujruygdjhmm'

# =========================
# INIT
# =========================

db.init_app(app)

mail.init_app(app)

# =========================
# BLUEPRINTS
# =========================

app.register_blueprint(auth)

app.register_blueprint(tramites)

app.register_blueprint(solicitudes)

# =========================
# CREATE TABLES
# =========================

with app.app_context():

    db.create_all()

# =========================
# RUN
# =========================

if __name__ == '__main__':

    app.run(host="0.0.0.0", port=5000)