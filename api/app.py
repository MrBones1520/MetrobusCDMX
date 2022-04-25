import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from model import CDMX
from flask.cli import FlaskGroup

app = Flask(__name__)

# Agregar grupo de comandos
cli = FlaskGroup(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")
db = SQLAlchemy(app)

cdmx = CDMX()


class AlcaldiaModel(db.Model):
    __tablename__ = "alcaldias"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    id_town = db.Column(db.Integer, unique=True, nullable=False)


class LineaMetroModel(db.Model):
    __tablename__ = "metrobus_lineas"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    simple_name = db.Column(db.String(80), unique=True, nullable=False)


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('created Tables')


def create_main_data():
    db.session.add_all()
    db.session.commit()
    print("main data created")


@app.route('/alcaldias', methods=['GET'])
def alcaldias_info():
    return cdmx.get_alcaldias_info(request.args)


@app.route('/metrobus', methods=['GET'])
def metrobus_info():
    return cdmx.get_lineas_info(request.args)


@cli.command("create_db")
def create_db():
    db.create_db()


if __name__ == '__main__':
    cli()
