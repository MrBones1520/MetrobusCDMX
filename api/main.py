import manage

from flask import Flask
from flask.cli import FlaskGroup
from flask import request

app = Flask(__name__)

cli = FlaskGroup(app)


@app.route('/alcaldias', methods=['GET'])
def alcaldias_all():
    return manage.resource_all_alcaldias(request.args)


@app.route('/alcaldias/<ide>', methods=['GET'])
def alcaldia(ide: int):
    return manage.resource_alcaldia(ide)


@app.route('/alcaldias-metrobus', methods=['GET'])
def alcaldia_compuest():
    return manage.resource_alcaldias_metrobus()


@app.route('/metrobus', methods=['GET'])
def metrobus_all():
    return manage.resource_all_metrobus(request.args)


@app.route('/metrobus-alcaldias', methods=['GET'])
def metrobus_compuest():
    return manage.resource_metrobus_alcaldias(request.args)


@app.route('/unidades', methods=['GET'])
def unidades_all():
    return manage.resource_all_unidades(request.args)


@app.route('/unidades/<ide>', methods=['GET'])
def unidad(ide: int):
    return manage.resource_unidad(ide)


@app.route('/unidades/status/<status>', methods=['GET'])
def unidad_by_status(status: int):
    return manage.resource_unidad_avaliable(status)


@cli.command("create_db")
def comm1():
    manage.create_db()


@cli.command("create_data")
def comm2():
    manage.create_data(manage)


@cli.command("update_data")
def comm3():
    manage.update_data(manage)


if __name__ == '__main__':
    cli()



