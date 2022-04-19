import json
from typing import List
from shapely.geometry import Polygon, Point
import pandas as pd


def get_coord(points: str) -> tuple:
    return tuple(map(float, points.split(',')))


class LineaMetro:

    def __init__(self, model):
        self.id = model['id']
        self.full_name = model['name']
        self.simple_name = model['nombre']
        self.geometry = json.loads(model['geometry'])
        self.id_line = model['line']
        self.operating = model['operating'] == 'yes'
        self.side = model['serv_side']
        self.point = Point(get_coord(model['geo_point_2d']))
        self.operative_days = model['oper_days']


class Alcaldia:

    def __init__(self, model, lines: List[LineaMetro]):
        self.id = model['id']
        self.name = model['nomgeo']
        self.point = Point(get_coord(model['geo_point_2d']))
        self.id_town = model['municipio']
        self.coordinates = json.loads(model['geo_shape'])['coordinates'][0]
        self.polygon = Polygon(self.coordinates)
        self.lineas_metro = list(filter(lambda lm: self.polygon.contains(lm.point), lines))


class CDMX:

    def __init__(self):
        self._df_alcaldias: pd.DataFrame = pd.read_csv('../data/alcaldias.csv')
        self._df_metro: pd.DataFrame = pd.read_csv('../data/concesionado_descriptor_cartografia.csv')
        self._metro = [LineaMetro(row) for _, row in self._df_metro.iterrows()]
        self._alcaldias = [Alcaldia(row, self._metro) for _, row in self._df_alcaldias.iterrows()]

    def get_alcadias_name(self) -> List[str]:
        return self._df_alcaldias['nomgeo'].tolist()

    def get_alcaldias(self) -> List[Alcaldia]:
        return self._alcaldias

    def get_lineas(self) -> List[LineaMetro]:
        return self._metro

    def get_lineas_full_name(self) -> List[str]:
        return self._df_metro['name']

