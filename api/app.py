from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from model import CDMX

app = Flask(__name__)
app.config.from_object("util.Configuration")
db = SQLAlchemy(app)
cdmx = CDMX()


@app.route('/alcaldias', methods=['GET'])
def alcaldias_info():
    return cdmx.get_alcaldias_info(request.args)


@app.route('/metrobus', methods=['GET'])
def metrobus_info():
    return cdmx.get_lineas_info(request.args)
