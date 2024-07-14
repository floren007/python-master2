import requests
import re
from io import BytesIO, StringIO
import zipfile
class UrlEMT:
    """
    DOCSTRING:
    Se crea la clase UrlEMT para recopilar todos los enlaces que haya en la web de la EMT
    """
    # Creamos 2 constantes
    EMT = 'https://opendata.emtmadrid.es/'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"
    # se Crea el init pero como el enunciado dice que este vacio
    
    def __init__(self):
        """
        La funcion init sirve para inicializar los atributos de la clase, en este caso me interesa actualizar
        los enlaces validos que recoje de la web
        """
        # creo un atributo llamado valid_urls 
        # que llama a la funcion select_valid_urls
        self.enlaces_validos = UrlEMT.select_valid_urls()
        # Esta funcion solo agarra los links que  son   validos

    
    @staticmethod
    def get_links(html_text: str) -> set:
        """
        Esta funcion sirve para obtener todos los enalces de la web EMT
        :param html_text: str
            texto en crudo de un html
        :return: set
            los inks devueltos indican que son los correctos

        >>> get_links("texto de la web que contiene links")
        set("link1","link3")
        """
        # Use regular expressions to find valid links
        link_pattern = r'<a[^>]*href="(/getattachment/[^"]+/trips_\d{2}_\d{2}_\w+-csv\.aspx)"[^>]*>.*?</a>'
        # un conjunto es una lista de objetos unicos por lo tanto el set() es la mejor opcion
        valid_links = set(re.findall(link_pattern, html_text))
        return valid_links

    
    def get_url(self,year: int,month: int) -> str:
        """
        Esta funcion sirve filtrar los enlaces y quedarnos con el que nos interesa
        para ello utilizo un patron que coincida que con los parametros que le hemos pasado
        en mi caso seria month = 12 y year = 22.
        Retorna el string de la url encontrada
        :param year: int
            Año del csv que queremos buscar
        :param month: int
            Mes del csv que queremos buscar
        :return: str
            Retorna el strig de la url encontrada
        >>> get_url(22,12)
            str("link encontrado")
        """

        # como solo son validos  los meses que son entre 1,12  y  el  año entre 2021  y 2023
        # hago un rango entre el año y los meses que nos interesan

        # Inicio de variable donde encuentra las url
        #urlEncontrado = None
        if month in range(1,13) and year in range(21,24):
            # con un patron que he creado, el cual le paso el año y el mes como si fuera un enlace
            # de string para posteriormente con la libreria search buscar ese patron entre todos los enlaces
            patron = f'{str(year)}_{str(month).zfill(2)}'
            # hacemos un bucle para recorrer todos los enlaces validos
            for url in self.enlaces_validos:
                # con la libreria re y la funcion search busca entre
                # todos los enlaces el patron que le he pasado como parametro
                # en el caso que lo encuentre nos salta una notificacion con la url encontrada
                if re.search(patron, url):
                    # para devolver el enlace totalmente correcto y listo para descargar
                    # para ello le sumamos el enlace de la pagina de bicimadrid como suijo
                    # y como prefijo el enlace descargado
                    urlEncontrado = self.EMT+url
                    print(f"Coincidió esta URL: {urlEncontrado}")
                    return urlEncontrado
                    #break
                else:
                    ValueError(f"No hay ningun enlace con tal año: {year} o mes: {month}")
        else:
            ValueError("No has introducido el año o el mes correcto")
    
    
    @staticmethod
    def select_valid_urls() -> set:
        """
        Método estático que se encarga de actualizar el atributo de los objetos de la clase. Devuelve un conjunto de enlaces válidos.
        :param None
        :return: set
            Devuelve un conjunto de enlaces válidos
        >>> select_valid_urls()
            set("link1","link2","link4")
        """
        try:
            # obtenemos el enlace de la web de bicimadrid
            response = requests.get(UrlEMT.EMT + UrlEMT.GENERAL)
            # hacemos un request a la web de bicimadrid
            # si el servidor esta activo y el enlace es correcto nos devolvera status code de 200 sino devolvera 400
            if response.status_code == 200:
                # obtenemos el texto de la web
                html_text = response.text
                # para enviarle el texto en crudo a la funcion get links
                # Creo que hubiera siso mucho mas sencillo hacerlo con web scraping
                # pero como hay que utilizar expresiones regulares pues le pasamos el texto en crudo
                valid_links = UrlEMT.get_links(html_text)
            else:
                raise ConnectionError("Conexion fallida")
            # retornamos el conjunto del links que son correctos
            return valid_links
        except ConnectionError as e:
            print(e)

    
    def get_csv(self,year: int,month: int) -> StringIO:
        """
        Esta funcion sirve para llamar a diferentes funciones con el resultado final que devuelve los datos del csv
        en fomato StringIO
        :param year: int
            Años del csv
        :param month: int
            Mes del año del csv
        :return: StringIO
            Retorna los datos del csv en formato StringIO
        >>> get_csv(22,12)
            StringIO(/x6/x8)
        """
        url = self.get_url(year, month)
        # ahora con el enlace devuelto lo que hacemos es pasarselo a la funcion csv_from_zip
        # para que nos saque los datos del csv, en este caso nos lo va devolver en StringIO 
        csv = UrlEMT.csv_from_zip(url)
        # se hace return de los datos del csv
        return csv
    
    
    @staticmethod
    def csv_from_zip(url: str) -> StringIO:
        """
        Esta funcion sirve para sacar los datos que hay dentro del csv.
        Se retorna en formato StringIO
        :param url:str
            Le pasa la url donde se encuentra el csv del que hay que obtener los datos
        :return: StringIO
            Devuelve la informacion que hay dentro del csv en formato StringIO

        >>> csv_from_zip("link1")
            StringIO(class "string.io")
        """    
        try:
            # le pasamos el enlace y lo que devuelve es a descarga del fichero
            file = requests.get(url)
            # ahora leemos el contenido en BytesIO
            file_content = BytesIO(file.content)
            # con la libreria zipfile podemos leer el contenido
            with zipfile.ZipFile(file_content, 'r') as zp:
                # se que el csv se encuentra en la primera posicion
                listar = zp.namelist()[0]
                # lo leo y lo codifico a utf-8 para podeer leerlo correctamente
                csv_textio = zp.read(listar).decode('utf-8')
                # por ultimo lo paso a StingIO
                string_csv = StringIO(csv_textio)
        except ConnectionError as e:
            print(e)
            # se retorna el csv en formato StringIO
        return string_csv


