from flask import Blueprint
from flask import render_template
from flask import request

from models.tramite import Tramite

tramites = Blueprint('tramites', __name__)


@tramites.route('/tramites')
def lista_tramites():

    categoria = request.args.get('categoria')
    busqueda = request.args.get('buscar')

    # BUSCADOR

    if busqueda:

        tramites_db = Tramite.query.filter(

            Tramite.nombre.ilike(f"%{busqueda}%")

        ).all()

    # FILTRO POR CATEGORÍA

    elif categoria:

        tramites_db = Tramite.query.filter_by(
            categoria=categoria,
            activo=True
        ).all()

    # TODOS

    else:

        tramites_db = Tramite.query.filter_by(
            activo=True
        ).all()

    return render_template(
        'tramites.html',
        tramites=tramites_db,
        categoria_actual=categoria
    )