import json
import requests
import pandas as pd

from util import group_by, get_coord
from typing import List, Optional
from shapely.geometry import Polygon, Point, LineString
from werkzeug.datastructures import MultiDict


class LineaMetro:

    keys_alter = {
        'lineas': 'simple_name',
        "operativo": 'operating'
    }

    @staticmethod
    def is_key_comp(key) -> bool:
        return key in LineaMetro.keys_alter

    @staticmethod
    def get_alter_name_attr(key_attr) -> str:
        return LineaMetro.keys_alter.get(key_attr)

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

    @staticmethod
    def is_key_comp(key) -> bool:
        return key in Alcaldia.keys_alter

    @staticmethod
    def get_alter_name_attr(key_attr) -> str:
        return Alcaldia.keys_alter.get(key_attr)

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


# Clase CDMX Singleton
class CDMX:

    _INSTANCE = None

    def __init__(self):
        _ml = requests.get(
            'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=61fd8d85-9598-4dfe-890b-2780ed26efc8'
        )
        _alc = requests.get(
            'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id=e4a9b05f-c480-45fb-a62c-6d4e39c5180e'
        )
        if _alc.status_code == 200:
            self._df_alcaldias: pd.DataFrame = pd.DataFrame(_alc.json()['result']['records'])
        if _ml.status_code == 200:
            self._df_metro: pd.DataFrame = pd.DataFrame(_ml.json()['result']['records'])
        self._metrobus = [LineaMetro(row) for _, row in self._df_metro.iterrows()]
        self._alcaldias = [Alcaldia(row, self._metrobus) for _, row in self._df_alcaldias.iterrows()]

    def __call__(self, *args, **kwargs):
        if not self._INSTANCE:
            self._INSTANCE = super().__call__(*args, **kwargs)
        return self._INSTANCE

    def get_unidades_info(self, args: MultiDict):
        _df_unidades = pd.read_csv('prueba_fetchdata_metrobus.csv')
        _unidades = [Unidad(row) for _, row in _df_unidades.iterrows()]

        value = sorted(
            list(map(lambda it: it.get_response(), _unidades)),
            key=lambda it: it['id']
        )
        return {"unidades": value}

    def get_alcaldias_info(self, args: MultiDict):
        arg0 = args.get('group-by')
        if arg0:
            value = group_by(
                self._alcaldias,
                lambda it: it.get_response(args),
                Alcaldia.get_alter_name_attr(arg0)
            )
        else:
            value = list(map(lambda it: it.get_response(args), self._alcaldias))

        return {'alcaldias': value}

    def get_lineas_info(self, args: MultiDict):
        arg0 = args.get('group-by')
        if arg0:
            value = group_by(
                self._metrobus,
                lambda it: it.get_response(args),
                LineaMetro.get_alter_name_attr(arg0)
            )
        else:
            value = list(map(lambda it: it.get_response(args), self._metrobus))

        return {'lineas': value}

    def get_unidad(self, id_: int):
        return {'unidad': {}}

    @property
    def alcaldias(self):
        return self._alcaldias

    @property
    def linea_metrobus(self):
        return self._metrobus


class Unidad:

    keys_alter = {
        'alcaldia': 'alcaldia_name',
        "status": 'operating'
    }

    @staticmethod
    def get_alter_name_attr(key_attr) -> str:
        return Unidad.keys_alter.get(key_attr)

    cdmx = CDMX()

    def __init__(self, model):
        self.id = model['vehicle_id']
        self.status = model['vehicle_current_status']
        self.point = Point(model['position_longitude'], model['position_latitude'])
        self.speed = model['position_speed']
        self.label = model['vehicle_label']
        self.route = model['trip_route_id']

    def __eq__(self, other):
        return self.id == other.id

    def get_alcaldia(self) -> Optional[Alcaldia]:
        for alcaldia in self.cdmx.alcaldias:
            if alcaldia.polygon.contains(self.point):
                return alcaldia
        return None

    def get_lm(self) -> Optional[LineaMetro]:
        for lm in self.cdmx.linea_metrobus:
            if lm.line_string.contains(self.point):
                return lm
        return None

    def get_response(self):
        alcaldia = self.get_alcaldia()
        linea = self.get_lm()
        return {
            'id': self.id,
            'status': self.status,
            'alcaldiaActual': alcaldia.get_response({})['name'] if alcaldia else None,
            "lmActual": linea.get_response({}) if linea else None,
            'latitude': self.point.x,
            'longitude': self.point.y,
        }
