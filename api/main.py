from flask import Flask, request
from flask.cli import FlaskGroup
import command
import model

app = Flask(__name__)

cdmx = model.CDMX()

# Agregar grupo de comandos
cli = FlaskGroup(app)


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


@cli.command("create_db")
def comm1():
    command.create_db()


@cli.command("create_data")
def comm2():
    command.create_data(cdmx)


if __name__ == '__main__':
    cli()



