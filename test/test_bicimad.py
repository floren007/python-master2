from bicimad import BiciMad
import pandas as pd
import pytest
import io
import numpy as np

"""
En este test, compruebo que los parametros son los correctos
y ademas
que algunas columnas tienen el tipo de dato correcto.
"""
def test_init():
    bici = BiciMad(month=12,year=22)
    assert bici.__dict__['_month'] == 12
    assert bici.__dict__['_year'] == 22
    df_types = bici.__dict__['_data'].dtypes
    assert df_types['idBike'] == np.float64
    assert df_types['geolocation_unlock'] == object
    assert isinstance(bici._data, pd.DataFrame)



"""
Este test comprubea que la funcion resume devuelve un pandas Series
"""
def test_type_resume():
    bici = BiciMad(month=12,year=22)
    assert type(bici.resume()) is pd.Series
"""
En esta funcion compruebo que las dimensiones del dataframe son correctas
"""
def test_data():
    bici = BiciMad(month=12,year=22)
    assert bici.data.shape == (493140, 15)

"""
En esta funcion compruebo que el dataframe ya no tiene valores nulos
"""
def test_data_is_null():
    bici = BiciMad(month=12,year=22)
    bici.clean()
    assert bici.data.isnull().sum() > 1
"""
En esta funcion se comprueba que el tipo de dato que devuelve es un pandas dataframe
"""
def test_get_data():
    isDF = BiciMad.get_data(month=12,year=22)
    assert type(isDF) is pd.DataFrame

"""
En esta funcion se comprueba que el tipo de dato que devuelve la funcion total_time es un pandas Series
"""
def test_total_time():
    bici = BiciMad(month=12,year=22)
    assert isinstance(bici.get_data(month=12,year=22), pd.DataFrame)
    assert isinstance(bici.most_popular_stations(), pd.Series)


