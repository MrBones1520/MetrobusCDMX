import os
from flask import Flask, request
from model import CDMX
from flask.cli import FlaskGroup

app = Flask(__name__)

# Agregar grupo de comandos
cli = FlaskGroup(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")

cdmx = CDMX()


@app.route('/alcaldias', methods=['GET'])
def alcaldias_info():
    return cdmx.get_alcaldias_info(request.args)


@app.route('/metrobus', methods=['GET'])
def metrobus_info():
    return cdmx.get_lineas_info(request.args)


@app.route('/unidades', methods=['GET'])
def unidades_info():
    return cdmx.get_unidades_info(request.args)


@app.route('/unidades/<ide>', methods=['GET'])
def unidad(ide: int):
    return cdmx.get_unidad(ide)


if __name__ == '__main__':
    cli()



