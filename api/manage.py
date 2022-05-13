import pandas as pd
import typing as typ

from model import *
from cachetools import cached, TTLCache
from requests import get
from werkzeug.datastructures import MultiDict


CDMX_DATA_URL = 'https://datos.cdmx.gob.mx/api/3/action/datastore_search?resource_id='

""" Obtaing Data"""


@cached(cache=TTLCache(maxsize=1024, ttl=300))
def get_df_alcaldias() -> pd.DataFrame:
    _alc = get(CDMX_DATA_URL + 'e4a9b05f-c480-45fb-a62c-6d4e39c5180e')
    return pd.DataFrame(_alc.json()['result']['records'])


@cached(cache=TTLCache(maxsize=512, ttl=300))
def get_df_metrobus() -> pd.DataFrame:
    ml = get(CDMX_DATA_URL + '61fd8d85-9598-4dfe-890b-2780ed26efc8')
    return pd.DataFrame(ml.json()['result']['records'])


def get_df_unidades() -> pd.DataFrame:
    return pd.read_csv('prueba_fetchdata_metrobus.csv')


""" Transformers """


def transform_alcaldias() -> typ.List[Alcaldia]:
    return list(map(Alcaldia, get_df_alcaldias().to_dict('records')))


def transform_metrobuses() -> typ.List[MetroBus]:
    return list(map(MetroBus, get_df_metrobus().to_dict('records')))


def transform_unidades() -> typ.List[Unidad]:
    return list(map(Unidad, get_df_unidades().to_dict('records')))


""" Responses """


@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_resources_comp():
    """Dict with Models Database"""
    return {
        'alcaldias': db.session.query(AlcaldiaModel).all(),
        'metrobus': db.session.query(MetroBusModel).all(),
        'unidades': db.session.query(UnidadModel).all()
    }


@cached(cache={})
def resource_all_unidades(args: MultiDict):
    """ List all Unidades """
    resources = get_resources_comp()
    responses = list(map(
        lambda it: UnidadModel.to(it).get_response(resources),
        resources['unidades']
    ))
    return {"unidades": responses}


def resource_all_alcaldias(args: MultiDict):
    """List all Alcaldias"""
    resources = get_resources_comp()
    responses = list(map(
        lambda it: AlcaldiaModel.to(it).get_response(),
        resources['alcaldias']
    ))
    return {'alcaldias': responses}


def resource_all_metrobus(args: MultiDict):
    """List all Metrobus"""
    metrobus = db.session.query(MetroBusModel).all()
    responses = list(map(
        lambda it: MetroBusModel.to(it).get_response(), metrobus
    ))
    return {'MetrobusLineas': responses}


def resource_alcaldia(ide: int):
    """Get Alcaldia by ID """
    alcaldia: AlcaldiaModel = db.session.query(AlcaldiaModel).get(ide)
    return {
        'alcaldia': AlcaldiaModel.to(alcaldia).get_response(get_resources_comp())
    }


def resource_unidad(id_unit: int):
    """Get Unidad by ID"""
    unidad = db.session.query(UnidadModel).get(id_unit)
    resources = get_resources_comp()
    return {'unidad': UnidadModel.to(unidad).get_response(resources)}


def resource_alcaldias_metrobus():
    """List All Alcaldias with Metrobus"""
    resources = get_resources_comp()
    lineas = list(map(MetroBusModel.to, resources['metrobus']))
    responses = list(map(
        lambda it: AlcaldiaModel.to(it).get_response_info(lineas),
        resources['alcaldias']
    ))
    return {'alcaldias': responses}


def resource_metrobus_alcaldias(args):
    """List all Metrobus in Alcaldias"""
    resources = get_resources_comp()
    alcaldias_man = list(map(AlcaldiaModel.to, resources['alcaldias']))
    responses = list(map(
        lambda it: MetroBusModel.to(it).get_response_info(alcaldias_man),
        resources['metrobus']
    ))
    return {'lineas': responses}


def resource_unidad_avaliable(status):
    """List All unidades with status"""
    unidades = db.session.query(UnidadModel).filter_by(status=status).all()
    responses = list(map(
        lambda it: UnidadModel.to(it).get_response(get_resources_comp()), unidades
    ))
    return {'unidades': responses}


""" Database Model Mapping"""


def models_alcaldias() -> typ.List[AlcaldiaModel]:
    return list(map(lambda it: it.entity, transform_alcaldias()))


def models_unidades() -> typ.List[UnidadModel]:
    return list(map(lambda it: it.entity, transform_unidades()))


def models_metrobus() -> typ.List[MetroBusModel]:
    return list(map(lambda it: it.entity, transform_metrobuses()))
