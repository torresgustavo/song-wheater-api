import os
import pytest
from pytest_httpx import HTTPXMock

from domain.enums.weather_unit_enum import WeatherMetricEnum
from domain.shared.errors.not_found_error import NotFoundError
from domain.shared.errors.unexpected_client_error import UnexpectedClientError
from infra.weather_client.open_weather_api.open_weather_api_client import (
    OpenWeatherApiClient,
)

__base_url = os.getenv("WHEATER_API_URL")
__secret = os.getenv("WHEATER_API_SECRET")


def test_should_success(httpx_mock: HTTPXMock):
    # Arrange
    client = OpenWeatherApiClient()

    city = "citytest"
    units = "metric"

    expected_metric = WeatherMetricEnum.CELSIUS

    httpx_mock.add_response(
        method="GET",
        url=f"{__base_url}/weather?q={city}&appid={__secret}&units={units}",
        json={"main": {"temp": 25.01}, "name": city, "sys": {"country": "BR"}},
    )

    # Act
    wheater = client.fetch_weather_data(location=city, metric=expected_metric)

    # Assert
    requests = httpx_mock.get_requests()
    assert len(requests) == 1

    assert wheater.city == city
    assert wheater.country == "BR"
    assert wheater.temperature == 25.01
    assert wheater.metric == expected_metric.value


def test_should_unexpected_response_format(httpx_mock: HTTPXMock):
    # Arrange
    client = OpenWeatherApiClient()

    city = "citytest"
    units = "metric"

    expected_metric = WeatherMetricEnum.CELSIUS

    prop_accessed = "'main'"
    new_unexpected_prop = "mainchanged"
    expected_error_message = (
        f"Unexpected response from OpenWeatherApiClient - {prop_accessed}"
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{__base_url}/weather?q={city}&appid={__secret}&units={units}",
        json={
            new_unexpected_prop: {"temp": 25.01},
            "name": city,
            "sys": {"country": "BR"},
        },
    )

    # Act
    with pytest.raises(UnexpectedClientError) as ex:
        client.fetch_weather_data(location=city, metric=expected_metric)

    # Assert
    requests = httpx_mock.get_requests()
    assert len(requests) == 1
    assert str(ex.value) == expected_error_message


def test_should_city_not_found_error(httpx_mock: HTTPXMock):
    # Arrange
    client = OpenWeatherApiClient()

    city = "citytest"
    units = "metric"

    expected_metric = WeatherMetricEnum.CELSIUS
    expected_response = {"error": "city not found"}

    httpx_mock.add_response(
        method="GET",
        url=f"{__base_url}/weather?q={city}&appid={__secret}&units={units}",
        status_code=404,
        json=expected_response,
    )

    # Act
    with pytest.raises(NotFoundError) as ex:
        client.fetch_weather_data(location=city, metric=expected_metric)

    # Assert
    assert ex.value.error_code == "NOT_FOUND"
    assert ex.value.message == "OpenWeatherApiClient - Not found weather to citytest"


@pytest.mark.parametrize("status_code", [400, 500, 502, 503, 504])
def test_should_unexpected_error(httpx_mock: HTTPXMock, status_code: int):
    # Arrange
    client = OpenWeatherApiClient()

    city = "citytest"
    units = "metric"

    expected_metric = WeatherMetricEnum.CELSIUS
    expected_response = {"error": "city not found"}

    httpx_mock.add_response(
        method="GET",
        url=f"{__base_url}/weather?q={city}&appid={__secret}&units={units}",
        status_code=status_code,
        json=expected_response,
    )

    # Act
    with pytest.raises(UnexpectedClientError) as ex:
        client.fetch_weather_data(location=city, metric=expected_metric)

    # Assert
    assert ex.value.error_code == "UNEXPECTED_CLIENT_ERROR"
