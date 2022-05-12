from flask import Flask, request
from flask.cli import FlaskGroup

import manage

app = Flask(__name__)

# Agregar grupo de comandos
cli = FlaskGroup(app)


@app.route('/alcaldias', methods=['GET'])
def alcaldias_info():
    return manage.get_alcaldias_info(request.args)


@app.route('/metrobus', methods=['GET'])
def metrobus_info():
    return manage.get_lineas_info(request.args)


@app.route('/unidades', methods=['GET'])
def unidades_info():
    return manage.get_unidades_info(request.args)


@app.route('/unidades/<ide>', methods=['GET'])
def unidad(ide: int):
    return manage.get_unidad(ide)


@cli.command("create_db")
def comm1():
    manage.create_db()


@cli.command("create_data")
def comm2():
    manage.create_data(manage)


if __name__ == '__main__':
    cli()



