import os
from flask_sqlalchemy import SQLAlchemy
import main
import model

main.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
main.app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")

db = SQLAlchemy(main.app)


class AlcaldiaModel(db.Model):
    __tablename__ = "alcaldias"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    id_town = db.Column(db.Integer, unique=True, nullable=False)

    @classmethod
    def of(cls, it: model.Alcaldia):
        return cls(name=it.name, id_town=it.id_town)


class LineaMetroModel(db.Model):
    __tablename__ = "metrobus_lineas"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    simple_name = db.Column(db.String(80), nullable=False)

    @classmethod
    def of(cls, it: model.LineaMetro):
        return cls(full_name=it.full_name, simple_name=it.simple_name)


class UnidadModel(db.Model):
    __tablename__ = "unidad"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    label = db.Column(db.String, nullable=True)
    point_x = db.Column(db.Float)
    point_y = db.Column(db.Float)

    @classmethod
    def of(cls, it: model.Unidad):
        return cls(
            status=it.status, label=it.label, point_x=it.point.x, point_y=it.point.y
        )

