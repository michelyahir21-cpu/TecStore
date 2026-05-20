from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import flash

from sqlalchemy.exc import IntegrityError

from database.bd import db
from models.user import User

auth = Blueprint('auth', __name__)

# =========================
# HOME
# =========================

@auth.route('/')
def home():

    return render_template(
        'index.html'
    )

# =========================
# REGISTER
# =========================

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        nControl = request.form['nControl'].strip()

        nombres = request.form['nombres'].strip()

        apellidoP = request.form['apellidoP'].strip()

        apellidoM = request.form['apellidoM'].strip()

        email = request.form['email'].strip().lower()

        password = request.form['password'].strip()

        # VALIDAR CAMPOS VACÍOS

        if not all([
            nControl,
            nombres,
            apellidoP,
            apellidoM,
            email,
            password
        ]):

            flash(
                'Todos los campos son obligatorios'
            )

            return redirect('/register')

        # VALIDAR EMAIL DUPLICADO

        usuario_existente = User.query.filter_by(
            email=email
        ).first()

        if usuario_existente:

            flash(
                'El correo ya está registrado'
            )

            return redirect('/register')

        # VALIDAR NÚMERO DE CONTROL

        control_existente = User.query.filter_by(
            nControl=nControl
        ).first()

        if control_existente:

            flash(
                'El número de control ya existe'
            )

            return redirect('/register')

        try:

            nuevo_usuario = User(
                nControl=nControl,
                nombres=nombres,
                apellidoP=apellidoP,
                apellidoM=apellidoM,
                email=email
            )

            nuevo_usuario.set_password(
                password
            )

            db.session.add(
                nuevo_usuario
            )

            db.session.commit()

            flash(
                'Usuario registrado correctamente'
            )

            return redirect('/login')

        except IntegrityError:

            db.session.rollback()

            flash(
                'Error de integridad en la base de datos'
            )

            return redirect('/register')

        except Exception:

            db.session.rollback()

            flash(
                'Ocurrió un error inesperado'
            )

            return redirect('/register')

    return render_template(
        'register.html'
    )

# =========================
# LOGIN
# =========================

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        login = request.form['login'].strip()

        password = request.form['password'].strip()

        # VALIDAR CAMPOS VACÍOS

        if not login or not password:

            flash(
                'Completa todos los campos'
            )

            return redirect('/login')

        usuario = User.query.filter(
            (User.email == login) |
            (User.nControl == login)
        ).first()

        if usuario and usuario.check_password(password):

            session.clear()

            session['user_id'] = usuario.nControl

            session['user_name'] = (
                f"{usuario.nombres} "
                f"{usuario.apellidoP}"
            )

            return redirect('/dashboard')

        flash(
            'Correo/Número de control '
            'o contraseña incorrectos'
        )

    return render_template(
        'login.html'
    )

# =========================
# DASHBOARD
# =========================

@auth.route('/dashboard')
def dashboard():

    if 'user_id' not in session:

        return redirect('/login')

    return render_template(
        'dashboard.html'
    )

# =========================
# LOGOUT
# =========================

@auth.route('/logout')
def logout():

    session.clear()

    flash(
        'Sesión cerrada correctamente'
    )

    return redirect('/')