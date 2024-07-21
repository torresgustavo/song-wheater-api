from abc import ABC, abstractmethod

from domain.entities.weather import Weather
from domain.enums.weather_unit_enum import WeatherMetricEnum


class WeatherApiClient(ABC):

    __name = None

    @abstractmethod
    def fetch_weather_data(self, location: str, metric: WeatherMetricEnum) -> Weather:
        raise NotImplementedError()
