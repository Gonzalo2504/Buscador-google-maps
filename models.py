import googlemaps
import requests

class BuscadorFarmacias:
    """
    Clase para buscar y obtener detalles de farmacias cercanas utilizando la API de Google Maps.
    """

    def __init__(self, api_key):
        """
        Inicializa un objeto BuscadorFarmacias con la clave de la API de Google Maps.

        Args:
            api_key (str): Clave de la API de Google Maps.
        """
        self.clave = googlemaps.Client(key=api_key)
        self.clave_api = api_key
        self.resultados = None  # Inicializar resultados en None
        self.detalles_list = []  # Inicializar la lista de detalles

    def obtener_ubicacion_usuario(self):
        """
        Obtiene la ubicación del usuario utilizando la API de Google Maps.

        Returns:
            tuple: Tupla con la latitud y longitud de la ubicación del usuario.
        """
        ubicacion = self.clave.geolocate()
        latitud = ubicacion["location"]["lat"]
        longitud = ubicacion["location"]["lng"]
        return latitud, longitud

    def buscar_y_obtener_detalles_farmacias(self, latitud, longitud, radio=10000, tipo_lugar="pharmacy", campos=None):
        """
        Busca y obtiene detalles de farmacias cercanas utilizando la API de Google Places.

        Args:
            latitud (float): Latitud de la ubicación desde donde se realizará la búsqueda.
            longitud (float): Longitud de la ubicación desde donde se realizará la búsqueda.
            radio (int, optional): Radio de búsqueda en metros (por defecto es 10000).
            tipo_lugar (str, optional): Tipo de lugar a buscar (por defecto es "pharmacy").
            campos (list[str], optional): Lista de campos a incluir en los detalles de cada lugar (por defecto son ["name", "formatted_address", "formatted_phone_number", "website", "rating"]).

        Returns:
            list: Lista de detalles de farmacias encontradas.
        """
        if campos is None:
            campos = [
                "name",
                "formatted_address",
                "formatted_phone_number",
                "website",
                "rating"
            ]

        consulta = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitud},{longitud}&radius={radio}&type={tipo_lugar}&key={self.clave_api}"

        respuesta = requests.get(consulta)

        if respuesta.status_code == 200:
            print("Conexión exitosa")
            self.resultados = respuesta.json()
            self.detalles_list = []  # Reiniciar la lista de detalles antes de cada búsqueda

        for lugar in self.resultados.get("results", []):
            place_id = lugar.get("place_id")
            self.obtener_detalles_lugar(place_id, campos)

        return self.detalles_list

    def obtener_detalles_lugar(self, place_id, campos, api_key=None):
        """
        Obtiene los detalles de un lugar específico utilizando la API de Google Places.

        Args:
            place_id (str): ID único del lugar que se desea obtener.
            campos (list[str]): Lista de campos a incluir en los detalles del lugar.
            api_key (str, optional): Clave de la API de Google Maps (por defecto es la clave proporcionada al inicializar la clase).

        Returns:
            dict: Diccionario con los detalles del lugar.
        """
        if api_key is None:
            api_key = self.clave_api

        detalles_consulta = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields={','.join(campos)}&key={api_key}"
        detalles_respuesta = requests.get(detalles_consulta)

        if detalles_respuesta.status_code == 200:
            detalles_json = detalles_respuesta.json()
            detalles = detalles_json.get('result', {})
            if detalles:
                self.detalles_list.append(detalles)
            else:
                print(f"Detalles vacíos para place_id {place_id}")
        else:
            print(f"Error al obtener detalles para place_id {place_id}")
