import pytest
import json
import os
from src.nominatim_api import NominatimAPI

def load_test_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path) as f:
        data = f.read()
        if not data.strip():
            raise ValueError(f"Файл {file_path} пустой.")
        return json.loads(data)

class TestGeocoding:
    # Загрузка тестовых данных из файлов
    direct_geocoding_data = load_test_data('data/direct_geocoding_data.json')
    reverse_geocoding_data = load_test_data('data/reverse_geocoding_data.json')
    invalid_geocoding_data = load_test_data('data/invalid_geocoding_data.json')

    @pytest.mark.parametrize("data", direct_geocoding_data)
    def test_direct_geocoding(self, data):
        result = NominatimAPI.geocode_address(data['address'])
        assert result, f"API геокодирования не вернуло результаты для адреса: {data['address']}"
        assert abs(float(result[0]['lat']) - float(data['expected_lat'])) < 0.01, f"Широта для {data['address']} некорректна"
        assert abs(float(result[0]['lon']) - float(data['expected_lon'])) < 0.01, f"Долгота для {data['address']} некорректна"

    @pytest.mark.parametrize("data", reverse_geocoding_data)
    def test_reverse_geocoding(self, data):
        result = NominatimAPI.reverse_geocode(data['lat'], data['lon'])
        assert result, f"API обратного геокодирования не вернуло результаты для координат: ({data['lat']}, {data['lon']})"
        assert 'city' in result['address'], f"Город не найден в адресе для координат: ({data['lat']}, {data['lon']})"
        assert data['expected_city'] in result['address']['city'], f"Название города для координат ({data['lat']}, {data['lon']}) некорректно"

    @pytest.mark.parametrize("data", invalid_geocoding_data)
    def test_invalid_geocoding(self, data):
        if 'address' in data:
            result = NominatimAPI.geocode_address(data['address'])
        else:
            result = NominatimAPI.reverse_geocode(data['lat'], data['lon'])
        
        assert not result, f"API геокодирования вернуло неожиданные результаты для данных: {data}"
        assert data['expected_error'] in "No results found"  # Проверка сообщения об ошибке

if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "tests/test_geocoding.py"])