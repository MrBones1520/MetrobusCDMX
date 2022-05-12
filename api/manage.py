# Clase CDMX Singleton
import db
import pandas as pd
import util

from model import LineaMetro, Alcaldia, Unidad, get_alter_name_attr
from requests import get
from werkzeug.datastructures import MultiDict


class CDMX:
    """Singleton Class"""
    _INSTANCE = None
    CDMX_DATA_URL = 'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id='

    def __init__(self):
        _ml = get(self.CDMX_DATA_URL + '61fd8d85-9598-4dfe-890b-2780ed26efc8')
        _alc = get(self.CDMX_DATA_URL + 'e4a9b05f-c480-45fb-a62c-6d4e39c5180e')
        if not (_alc.status_code == 200 and _ml.status_code == 200):
            Exception("No Origin Data Request")
        self._df_alcaldias: pd.DataFrame = pd.DataFrame(_alc.json()['result']['records'])
        self._df_metro: pd.DataFrame = pd.DataFrame(_ml.json()['result']['records'])
        self._df_unidades: pd.DataFrame = pd.read_csv('prueba_fetchdata_metrobus.csv')
        self._metrobus = [LineaMetro(row) for _, row in self._df_metro.iterrows()]
        self._alcaldias = [Alcaldia(row, self._metrobus) for _, row in self._df_alcaldias.iterrows()]
        self._unidades = [Unidad(it) for it in self._df_unidades.to_dict('records')]

    def __call__(self, *args, **kwargs):
        if not self._INSTANCE:
            self._INSTANCE = super().__call__(*args, **kwargs)
        return self._INSTANCE

    def get_unidades_info(self, args: MultiDict):
        value = sorted(
            list(map(lambda it: it.get_response(), self._unidades)),
            key=lambda it: it['vehicleId']
        )
        return {"unidades": value}

    def get_alcaldias_info(self, args: MultiDict):
        arg0 = args.get('group-by')
        if arg0:
            value = util.group_by(
                self._alcaldias,
                lambda it: it.get_response(args),
                get_alter_name_attr('alc', arg0)
            )
        else:
            value = list(map(lambda it: it.get_response(args), self._alcaldias))

        return {'alcaldias': value}

    def get_lineas_info(self, args: MultiDict):
        arg0 = args.get('group-by')
        if arg0:
            value = util.group_by(
                self._metrobus,
                lambda it: it.get_response(args),
                get_alter_name_attr('lm', arg0)
            )
        else:
            value = list(map(lambda it: it.get_response(args), self._metrobus))

        return {'lineas': value}

    def get_unidad(self, id_: int):
        value = filter(lambda it: it.vehicle_id == id_, self._unidades)
        if not value:
            return {'status': False}
        return {'unidad': value.get_response()}

    @property
    def alcaldias_model(self):
        return [db.AlcaldiaModel.of(it) for it in self._alcaldias]

    @property
    def linea_metrobus_model(self):
        return [db.LineaMetroModel.of(it) for it in self._metrobus]

    @property
    def unidades_model(self):
        return [db.UnidadModel.of(it) for it in self._unidades]
