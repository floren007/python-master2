#from aiohttp import request

from bicimad import UrlEMT
import io
import pytest
import requests

"""
Esta funcion sirve para comprobrar que los enlaces son correctos
"""
def test_constantes_clase():
    assert UrlEMT.EMT == 'https://opendata.emtmadrid.es/'
    assert UrlEMT.GENERAL == "/Datos-estaticos/Datos-generales-(1)"

""" 
Esta funcion comprueba que el enlace que devuelve get_links es correcto
"""
def test_url_get_links():
    class_emt = UrlEMT()
    req = requests.get(class_emt.EMT, class_emt.GENERAL)
    html = req.text
    url_valida = class_emt.get_links(html)
    assert len(url_valida) == 21

"""
Esta funcion comprueba que los datos devueltos del csv estan en formato StringIO
"""
def test_csv_from_zip():
    class_emt = UrlEMT()
    url_correcta = "https://opendata.emtmadrid.es//getattachment/34b933e4-4756-4fed-8d5b-2d44f7503ccc/trips_22_12_December-csv.aspx"
    csv = class_emt.csv_from_zip(url_correcta)
    assert type(csv) is io.StringIO

"""
Esta funcion es igual que a la anterior ya que no tengo mucho mas que comprobar

compruebo que la funcion devuelta es un StringIO
"""
def test_get_csv():
    class_emt = UrlEMT()
    csv = class_emt.get_csv(22,12)
    assert type(csv) is io.StringIO


"""
Esta funcion comprueba que la url que devuelve la funcion get_url es correcta
"""
def test_get_url():
    class_emt = UrlEMT()
    url_valida = class_emt.get_url(month=12, year=22)
    assert url_valida == "https://opendata.emtmadrid.es//getattachment/34b933e4-4756-4fed-8d5b-2d44f7503ccc/trips_22_12_December-csv.aspx"

"""
Esta funcion sirve para comrpobar que el request que le estamos haciendo a la web EMT es correcto
si el servidor esta funcionando nos devolvera un 200 pero en cambio si el servidor se ha caido nos devolvera un 400
"""
def test_select_valid_urls():
    class_emt = UrlEMT()
    class_emt.select_valid_urls()
    comprobar = requests.get(UrlEMT.EMT + UrlEMT.GENERAL)
    assert comprobar.status_code == 200