import json
import util
import os

from main import app
from typing import List
from flask_sqlalchemy import SQLAlchemy
from shapely.geometry import Polygon, Point, LineString

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite://")

db = SQLAlchemy(app)


""" Class Checker """


class MetroBus:

    @property
    def entity(self):
        return MetroBusModel.of(self)

    def __init__(self, data):
        self.id = data['id']
        self.id_line = data['line']
        self.full_name = data['name']
        self.simple_name = data['nombre']
        self.geometry = json.dumps(data['geometry'])
        self.coordinates = json.loads(data['geometry'])['coordinates']
        self.line_string = LineString(self.coordinates)
        self.operating = data['operating'] == 'yes'
        self.side = data['serv_side']
        self.point = Point(util.get_coord(data['geo_point_2d']))
        self.operative_days = data['oper_days']

    def get_response(self) -> dict:
        return {
            "id": self.id,
            "idLine": self.id_line,
            "name": self.simple_name,
            "fullName": self.full_name,
            "operating": self.operating,
            "sideService": self.side,
            "operativeDays": self.operative_days,
        }


class Alcaldia:

    @property
    def entity(self):
        return AlcaldiaModel.of(self)

    def __init__(self, data):
        self.id = data['id']
        self.name = data['nomgeo']
        self.point = Point(util.get_coord(data['geo_point_2d']))
        self.id_town = data['municipio']
        self.shape = json.dumps(data['geo_shape'])
        self.coordinates = json.loads(data['geo_shape'])['coordinates'][0]
        self.polygon = Polygon(self.coordinates)

    def get_response(self):
        return {
            'id': self.id,
            'name': self.name,
            "latitud": self.point.x,
            "longitud": self.point.y
        }

    def get_response_info(self, lines: List[MetroBus]):
        lines = list(filter(
            lambda lm: lm.line_string.intersects(self.polygon), lines
        ))
        return {
            **self.get_response(),
            "lines": list(map(MetroBus.get_response, lines))
        }


class Unidad:

    @property
    def entity(self):
        return UnidadModel.of(self)

    def __init__(self, model):
        self.vehicle_id = model['vehicle_id']
        self.status = model['vehicle_current_status']
        self.point = Point(model['position_longitude'], model['position_latitude'])
        self.speed = model['position_speed']
        self.label = model['vehicle_label']
        self.route = model['trip_route_id']

    def get_response(self):
        return {
            'vehicleId': self.vehicle_id,
            'status': self.status,
            'latitude': self.point.x,
            'longitude': self.point.y,
        }


""" Model Database """


class AlcaldiaModel(db.Model):
    __tablename__ = "alcaldia"

    @classmethod
    def of(cls, it: Alcaldia):
        return cls(
            id=it.id,
            name=it.name,
            id_town=it.id_town,
            polygon=str(it.polygon),
            coord_x=it.point.x,
            coord_y=it.point.y,
            shape=it.shape,
        )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    id_town = db.Column(db.Integer, unique=True, nullable=False)
    coord_x = db.Column(db.Float, nullable=False)
    coord_y = db.Column(db.Float, nullable=False)
    polygon = db.Column(db.String, nullable=False)
    shape = db.Column(db.String, nullable=False)

    def to(self) -> Alcaldia:
        return Alcaldia({
            'id': self.id,
            'nomgeo': self.name,
            'geo_point_2d': f"{self.coord_x}, {self.coord_y}",
            'municipio': self.id_town,
            'geo_shape': json.loads(self.shape),
        })


class MetroBusModel(db.Model):
    __tablename__ = "metrobus"

    @classmethod
    def of(cls, it: MetroBus):
        return cls(
            full_name=it.full_name,
            simple_name=it.simple_name,
            coord_x=it.point.x,
            coord_y=it.point.y,
            operative=it.operating,
            service_side=it.side,
            service_days=it.operative_days,
            id_line=it.id_line,
            geometry=it.geometry
        )

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    simple_name = db.Column(db.String(80), nullable=False)
    coord_x = db.Column(db.Float, nullable=False)
    coord_y = db.Column(db.Float, nullable=False)
    operative = db.Column(db.Boolean, nullable=False)
    service_side = db.Column(db.String, nullable=False)
    service_days = db.Column(db.String, nullable=False)
    id_line = db.Column(db.Integer, nullable=True)
    geometry = db.Column(db.String, nullable=False)

    def to(self) -> MetroBus:
        return MetroBus({
            'id': self.id,
            'line': self.id_line,
            'name': self.full_name,
            'nombre': self.simple_name,
            'geometry': json.loads(self.geometry),
            'serv_side': self.service_side,
            'oper_days': self.service_days,
            'operating': self.operative,
            'geo_point_2d': f"{self.coord_x}, {self.coord_y}"
        })


class AlcaldiaMetrobus(db.Model):
    __tablename__ = "alcaldia_metrobus"

    id = db.Column(db.Integer, primary_key=True)
    alcaldia_id = db.Column(db.Integer, nullable=False)
    metrobus_id = db.Column(db.Integer, nullable=False)


class UnidadModel(db.Model):
    __tablename__ = "unidad"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean)
    label = db.Column(db.String, nullable=True)
    point_x = db.Column(db.Float)
    point_y = db.Column(db.Float)
    speed = db.Column(db.Integer)
    trip_id = db.Column(db.Float)

    @classmethod
    def of(cls, it: Unidad):
        return cls(
            status=bool(it.status),
            label=it.label,
            point_x=it.point.x,
            point_y=it.point.y,
            speed=it.speed,
            trip_id=it.route
        )

    def to(self) -> Unidad:
        return Unidad({
            'vehicle_id': self.id,
            'vehicle_current_status': self.status,
            'position_longitude': self.point_x,
            'position_latitude': self.point_y,
            'position_speed': self.speed,
            "vehicle_label": self.label,
            'trip_route_id': self.trip_id
        })


""" Commands """


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print('created Tables')


def create_data(manage):
    create_db()
    db.session.add_all(manage.models_alcaldias())
    print("Created Alcaldias")
    db.session.add_all(manage.models_metrobus())
    print("Created Metrobus")
    db.session.add_all(manage.models_unidades())
    print("Created Unidades")
    db.session.commit()

