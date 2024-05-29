import requests

class NominatimAPI:
    BASE_URL = "https://nominatim.openstreetmap.org/"

    @staticmethod
    def geocode_address(address):
        """
        Выполняет прямое геокодирование для указанного адреса.

        :param address: Строка с адресом для геокодирования
        :return: JSON ответ с результатами геокодирования
        """
        response = requests.get(f"{NominatimAPI.BASE_URL}search", params={"q": address, "format": "json"})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def reverse_geocode(lat, lon):
        """
        Выполняет обратное геокодирование для указанных координат.

        :param lat: Широта
        :param lon: Долгота
        :return: JSON ответ с результатами геокодирования
        """
        response = requests.get(f"{NominatimAPI.BASE_URL}reverse", params={"lat": lat, "lon": lon, "format": "json"})
        response.raise_for_status()
        return response.json()