import json

from util import get_coord
from typing import List
from shapely.geometry import Polygon, Point, LineString


class LineaMetro:

    keys_alter = {
        'lineas': 'simple_name',
        "operativo": 'operating'
    }

    def __init__(self, model):
        self.id = model['id']
        self.id_line = model['line']
        self.full_name = model['name']
        self.simple_name = model['nombre']
        self.coordinates = json.loads(model['geometry'])['coordinates']
        self.line_string = LineString(self.coordinates)
        self.operating = model['operating'] == 'yes'
        self.side = model['serv_side']
        self.point = Point(get_coord(model['geo_point_2d']))
        self.operative_days = model['oper_days']

    def get_response(self, args=None) -> dict:
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

    keys_alter = {
        'lineas': 'simple_name',
        "operativo": 'operating'
    }

    def __init__(self, model, lines: List[LineaMetro]):
        self.id = model['id']
        self.name = model['nomgeo']
        self.point = Point(get_coord(model['geo_point_2d']))
        self.id_town = model['municipio']
        self.coordinates = json.loads(model['geo_shape'])['coordinates'][0]
        self.polygon = Polygon(self.coordinates)
        self.lineas_metro = list(
            filter(
                lambda lm: lm.line_string.intersects(self.polygon),
                lines
            )
        )

    def get_response(self, args):
        form = args.get('form')
        base = {
            "id": self.id,
            "name": self.name,
            "idTown": self.id_town,
        }
        if form == 'routes':
            lmb = list(map(LineaMetro.get_response, self.lineas_metro))
            return {
                **base,
                "lines": lmb,
                "linesCount": len(lmb),
            }

        return base


class Unidad:

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


def is_key_comp(id_class, key) -> bool:
    if id_class == 'lm':
        return key in LineaMetro.keys_alter
    return False


def get_alter_name_attr(id_class, key_attr) -> str:
    if id_class == 'lm':
        return LineaMetro.keys_alter.get(key_attr)
    if id_class == 'alc':
        return Alcaldia.keys_alter.get(key_attr)
    return ''
