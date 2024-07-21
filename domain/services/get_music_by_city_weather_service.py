from abc import ABC
from typing import List, Tuple

from domain.entities.music import Music
from domain.entities.weather import Weather
from domain.enums.music_genre_type_enum import MusicGenreTypeEnum
from domain.enums.weather_unit_enum import WeatherMetricEnum
from domain.interfaces.weather_api_client import WeatherApiClient
from domain.interfaces.music_api_client import MusicApiClient
from domain.shared.errors.not_found_error import NotFoundError


class GetMusicByCityWeatherService(ABC):

    def __init__(
        self, weather_client_api: WeatherApiClient, music_client_api: MusicApiClient
    ):
        self.__wheather_client_api = weather_client_api
        self.__music_client_api = music_client_api

    def execute(self, city: str) -> Tuple[Weather, List[Music]]:

        weather = self.__wheather_client_api.fetch_weather_data(
            location=city, metric=WeatherMetricEnum.CELSIUS
        )
        genre = self.__get_genre_by_weather(weather=weather)
        music_list = self.__music_client_api.fetch_music_by_genre(genre=genre)

        if len(music_list) == 0:
            raise NotFoundError(
                resource_name="Music",
                message="No music found",
                detail={"city": city, "genre": genre.value},
            )

        return weather, music_list

    def __get_genre_by_weather(self, weather: Weather) -> MusicGenreTypeEnum:
        if weather.temperature > 25:
            return MusicGenreTypeEnum.POP
        if 10 <= weather.temperature <= 25:
            return MusicGenreTypeEnum.ROCK
        else:
            return MusicGenreTypeEnum.CLASSICAL
