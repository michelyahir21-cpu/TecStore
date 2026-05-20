from database.bd import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    __tablename__ = 'users'

    nControl = db.Column(db.String(20), primary_key=True)

    nombres = db.Column(db.String(50), nullable=False)

    apellidoP = db.Column(db.String(100), nullable=False)

    apellidoM = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)