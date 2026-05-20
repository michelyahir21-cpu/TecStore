from database.bd import db


class Solicitud(db.Model):

    __tablename__ = 'solicitudes'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.String(20),
        nullable=False
    )

    tramite_id = db.Column(
        db.Integer,
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    estado = db.Column(
        db.String(50),
        default='Pendiente'
    )

    metodo_pago = db.Column(
        db.String(50)
    )

    pagado = db.Column(
        db.Boolean,
        default=False
    )
    folio = db.Column(
    db.String(50)
    )