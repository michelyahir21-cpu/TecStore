from database.bd import db


class Tramite(db.Model):

    __tablename__ = 'tramites'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(150), nullable=False)

    descripcion = db.Column(db.Text, nullable=False)

    categoria = db.Column(db.String(100), nullable=False)

    costo = db.Column(db.Float, nullable=False)

    tiempo = db.Column(db.String(50), nullable=False)

    requisitos = db.Column(db.Text, nullable=False)

    icono = db.Column(db.String(100), nullable=False)

    activo = db.Column(db.Boolean, default=True)