from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import flash
from flask import make_response

from reportlab.pdfgen import canvas

from io import BytesIO

from flask_mail import Message

from extensions import mail

from database.bd import db

from models.solicitud import Solicitud
from models.tramite import Tramite
from models.user import User

solicitudes = Blueprint(
    'solicitudes',
    __name__
)

# =========================
# PAGO
# =========================

@solicitudes.route('/pago/<int:tramite_id>')
def pago(tramite_id):

    if 'user_id' not in session:

        return redirect('/login')

    tramite = Tramite.query.get_or_404(
        tramite_id
    )

    return render_template(
        'pago.html',
        tramite=tramite
    )


# =========================
# CONFIRMAR PAGO
# =========================

@solicitudes.route(
    '/confirmar_pago/<int:tramite_id>',
    methods=['POST']
)
def confirmar_pago(tramite_id):

    if 'user_id' not in session:

        return redirect('/login')

    tramite = Tramite.query.get_or_404(
        tramite_id
    )

    metodo_pago = request.form.get(
        'metodo_pago'
    )

    # =========================
    # CREAR FOLIO
    # =========================

    total_solicitudes = (
        Solicitud.query.count() + 1
    )

    folio = (
        f"TEC-2026-{total_solicitudes:04}"
    )

    # =========================
    # GUARDAR SOLICITUD
    # =========================

    nueva_solicitud = Solicitud(

        usuario_id=session['user_id'],

        tramite_id=tramite_id,

        metodo_pago=metodo_pago,

        pagado=True,

        estado='Pagado',

        folio=folio

    )

    db.session.add(
        nueva_solicitud
    )

    db.session.commit()

    # =========================
    # USUARIO
    # =========================

    usuario = User.query.filter_by(

        nControl=session['user_id']

    ).first()

    # =========================
    # CREAR CORREO
    # =========================

    msg = Message(

        'Documento oficial TecStore',

        sender='TU_CORREO@gmail.com',

        recipients=[usuario.email]

    )

    msg.body = f"""

Hola {usuario.nombres}

Tu trámite:

{tramite.nombre}

ha sido generado correctamente.

Folio:
{folio}

Adjunto encontrarás tu documento.

Gracias por usar TecStore.

"""

    # =========================
    # CREAR PDF
    # =========================

    pdf_buffer = BytesIO()

    pdf = canvas.Canvas(pdf_buffer)

    # TITULO

    pdf.setFont(
        "Helvetica-Bold",
        20
    )

    pdf.drawString(
        170,
        800,
        "Documento Oficial"
    )

    # INFO

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        100,
        720,
        f"Alumno: {usuario.nombres}"
    )

    pdf.drawString(
        100,
        690,
        f"Trámite: {tramite.nombre}"
    )

    pdf.drawString(
        100,
        660,
        f"Folio: {folio}"
    )

    pdf.drawString(
        100,
        630,
        "Documento generado automáticamente."
    )

    pdf.drawString(
        100,
        600,
        "Instituto Tecnológico de Tláhuac II"
    )

    pdf.showPage()

    pdf.save()

    pdf_buffer.seek(0)

    # =========================
    # ADJUNTAR PDF
    # =========================

    msg.attach(

        f'{folio}.pdf',

        'application/pdf',

        pdf_buffer.read()

    )

    # =========================
    # ENVIAR
    # =========================

    mail.send(msg)

    flash(
        'Pago realizado correctamente.'
    )

    return redirect('/mis_tramites')


# =========================
# MIS TRÁMITES
# =========================

@solicitudes.route('/mis_tramites')
def mis_tramites():

    if 'user_id' not in session:

        return redirect('/login')

    solicitudes_db = Solicitud.query.filter_by(

        usuario_id=session['user_id']

    ).all()

    tramites_usuario = []

    for solicitud in solicitudes_db:

        tramite = Tramite.query.get(
            solicitud.tramite_id
        )

        tramites_usuario.append({

            'solicitud': solicitud,

            'tramite': tramite

        })

    return render_template(

        'mis_tramites.html',

        tramites_usuario=tramites_usuario

    )


# =========================
# PDF COMPROBANTE
# =========================

@solicitudes.route('/pdf/<int:solicitud_id>')
def generar_pdf(solicitud_id):

    if 'user_id' not in session:

        return redirect('/login')

    solicitud = Solicitud.query.get_or_404(
        solicitud_id
    )

    tramite = Tramite.query.get(
        solicitud.tramite_id
    )

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    # TITULO

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        180,
        800,
        "TecStore"
    )

    pdf.setFont(
        "Helvetica",
        16
    )

    pdf.drawString(
        150,
        770,
        "Comprobante de pago"
    )

    # INFO

    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        100,
        700,
        f"Alumno: {session['user_name']}"
    )

    pdf.drawString(
        100,
        670,
        f"Trámite: {tramite.nombre}"
    )

    pdf.drawString(
        100,
        640,
        f"Categoría: {tramite.categoria}"
    )

    pdf.drawString(
        100,
        610,
        f"Folio: {solicitud.folio}"
    )

    pdf.drawString(
        100,
        580,
        f"Método de pago: {solicitud.metodo_pago}"
    )

    pdf.drawString(
        100,
        550,
        f"Estado: {solicitud.estado}"
    )

    pdf.drawString(
        100,
        520,
        f"Fecha: {solicitud.fecha}"
    )

    pdf.showPage()

    pdf.save()

    buffer.seek(0)

    response = make_response(
        buffer.getvalue()
    )

    response.headers[
        'Content-Type'
    ] = 'application/pdf'

    response.headers[
        'Content-Disposition'
    ] = (
        f'inline; filename={solicitud.folio}.pdf'
    )

    return response