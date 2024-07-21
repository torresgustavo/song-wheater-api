from unittest.mock import Mock
import pytest

from domain.entities.music import Music
from domain.entities.weather import Weather
from domain.enums.music_genre_type_enum import MusicGenreTypeEnum
from domain.enums.weather_unit_enum import WeatherMetricEnum
from domain.interfaces.music_api_client import MusicApiClient
from domain.interfaces.weather_api_client import WeatherApiClient
from domain.services.get_music_by_city_weather_service import (
    GetMusicByCityWeatherService,
)
from domain.shared.errors.not_found_error import NotFoundError


class MockedWeatherApiClient(WeatherApiClient):
    def fetch_weather_data(self, location: str, metric: WeatherMetricEnum):
        pass


class MockedMusicApiClient(MusicApiClient):
    def fetch_music_by_genre(self, genre: MusicGenreTypeEnum):
        pass


@pytest.mark.parametrize(
    "temperature_returned, expected_genre",
    [
        (9.9, MusicGenreTypeEnum.CLASSICAL),
        (10.1, MusicGenreTypeEnum.ROCK),
        (24.9, MusicGenreTypeEnum.ROCK),
        (25.1, MusicGenreTypeEnum.POP),
    ],
)
def test_should_success(
    temperature_returned: float, expected_genre: MusicGenreTypeEnum
):
    # Arrange
    city_to_search = "test"

    mock_wheater_client_api = MockedWeatherApiClient()
    mock_wheater_client_api.fetch_weather_data = Mock(
        return_value=Weather(
            temperature=temperature_returned,
            city=city_to_search,
            country="BR",
            metric=WeatherMetricEnum.CELSIUS.value,
        )
    )
    mock_music_client_api = MockedMusicApiClient()
    mock_music_client_api.fetch_music_by_genre = Mock(
        return_value=[Music("test1", "artist_test")]
    )

    service = GetMusicByCityWeatherService(
        weather_client_api=mock_wheater_client_api,
        music_client_api=mock_music_client_api,
    )

    # Act
    result = service.execute(city=city_to_search)

    # Assert
    mock_wheater_client_api.fetch_weather_data.assert_called_once_with(
        location=city_to_search, metric=WeatherMetricEnum.CELSIUS
    )

    mock_music_client_api.fetch_music_by_genre.assert_called_once_with(
        genre=expected_genre
    )

    assert result[0].temperature == temperature_returned
    assert result[0].city == "test"
    assert result[0].country == "BR"
    assert result[0].metric == WeatherMetricEnum.CELSIUS.value
    assert result[1][0].name == "test1"
    assert result[1][0].artist == "artist_test"


@pytest.mark.parametrize(
    "temperature_returned, expected_genre",
    [
        (9.9, MusicGenreTypeEnum.CLASSICAL),
        (10.1, MusicGenreTypeEnum.ROCK),
        (24.9, MusicGenreTypeEnum.ROCK),
        (25.1, MusicGenreTypeEnum.POP),
    ],
)
def test_should_without_music_found(
    temperature_returned: float, expected_genre: MusicGenreTypeEnum
):
    # Arrange
    city_to_search = "test"

    mock_wheater_client_api = MockedWeatherApiClient()
    mock_wheater_client_api.fetch_weather_data = Mock(
        return_value=Weather(
            temperature=temperature_returned,
            city=city_to_search,
            country="BR",
            metric=WeatherMetricEnum.CELSIUS.value,
        )
    )
    mock_music_client_api = MockedMusicApiClient()
    mock_music_client_api.fetch_music_by_genre = Mock(return_value=[])

    service = GetMusicByCityWeatherService(
        weather_client_api=mock_wheater_client_api,
        music_client_api=mock_music_client_api,
    )

    # Act
    with pytest.raises(NotFoundError) as ex:
        service.execute(city=city_to_search)

    # Assert
    mock_wheater_client_api.fetch_weather_data.assert_called_once_with(
        location=city_to_search, metric=WeatherMetricEnum.CELSIUS
    )

    mock_music_client_api.fetch_music_by_genre.assert_called_once_with(
        genre=expected_genre
    )

    assert ex.value.message == "No music found"
    assert ex.value.detail == {"city": city_to_search, "genre": expected_genre.value}
