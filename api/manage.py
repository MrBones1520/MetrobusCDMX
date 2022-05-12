import pandas as pd
import typing as typ
import util

from model import *
from requests import get
from werkzeug.datastructures import MultiDict


CDMX_DATA_URL = 'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id='

""" Obtaing Data"""


def get_df_alcaldias() -> pd.DataFrame:
    _alc = get(CDMX_DATA_URL + 'e4a9b05f-c480-45fb-a62c-6d4e39c5180e')
    return pd.DataFrame(_alc.json()['result']['records'])


def get_df_metrobus() -> pd.DataFrame:
    ml = get(CDMX_DATA_URL + '61fd8d85-9598-4dfe-890b-2780ed26efc8')
    return pd.DataFrame(ml.json()['result']['records'])


def get_df_unidades() -> pd.DataFrame:
    return pd.read_csv('prueba_fetchdata_metrobus.csv')


""" Transformers """


def transform_alcaldias() -> typ.List[Alcaldia]:
    return list(map(Alcaldia, get_df_alcaldias().to_dict('records')))


def transform_metrobuses() -> typ.List[LineaMetro]:
    return list(map(LineaMetro, get_df_metrobus().to_dict('records')))


def transform_unidades() -> typ.List[Unidad]:
    return list(map(Unidad, get_df_unidades().to_dict('records')))


""" Responses """


def get_unidades_info(args: MultiDict):
    value = sorted(
        list(map(lambda it: it.get_response(), transform_unidades())),
        key=lambda it: it['vehicleId']
    )
    return {"unidades": value}


def get_alcaldias_info(args: MultiDict):
    arg0 = args.get('group-by')
    alcaldias = transform_alcaldias()
    if arg0:
        value = util.group_by(
            alcaldias,
            lambda it: it.get_response(args),
            get_alter_name_attr('alc', arg0)
        )
    else:
        value = list(map(lambda it: it.get_response(args), alcaldias))

    return {'alcaldias': value}


def get_lineas_info(args: MultiDict):
    arg0 = args.get('group-by')
    metrobus = transform_metrobuses()
    if arg0:
        value = util.group_by(
            metrobus,
            lambda it: it.get_response(args),
            get_alter_name_attr('lm', arg0)
        )
    else:
        value = list(map(lambda it: it.get_response(args), metrobus))

    return {'lineas': value}


def get_unidad(id_unit: int):
    unidades = transform_unidades()
    value = filter(lambda it: it.vehicle_id == id_unit, unidades)
    if not value:
        return {'status': False}
    return {'unidad': value.get_response()}


""" Database Model Mapping"""


def models_alcaldias() -> typ.List[AlcaldiaModel]:
    return list(map(lambda it: it.entity, transform_alcaldias()))


def models_unidades() -> typ.List[UnidadModel]:
    return list(map(lambda it: it.entity, transform_unidades()))


def models_metrobus() -> typ.List[MetroBusModel]:
    return list(map(lambda it: it.entity, transform_metrobuses()))

