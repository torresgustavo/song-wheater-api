import os
import httpx

from domain.shared.errors.not_found_error import NotFoundError
from extensions.log_extension import get_logger

from domain.entities.weather import Weather
from domain.interfaces.weather_api_client import WeatherApiClient
from domain.enums.weather_unit_enum import WeatherMetricEnum
from domain.shared.errors.unexpected_client_error import UnexpectedClientError


class OpenWeatherApiClient(WeatherApiClient):

    __name = "OpenWeatherApiClient"
    __open_weather_unit = {
        WeatherMetricEnum.CELSIUS.value: "metric",
        WeatherMetricEnum.FAHRENHEIT.value: "imperial",
        WeatherMetricEnum.KELVIN.value: "standard",
    }

    def __init__(self):

        self.__logger = get_logger(__name__)
        self.__base_url = os.getenv("WHEATER_API_URL")
        self.__secret = os.getenv("WHEATER_API_SECRET")

        self.__client = httpx.Client(base_url=self.__base_url)

    def fetch_weather_data(self, location: str, metric: WeatherMetricEnum) -> Weather:
        query_params = {
            "q": location,
            "appid": self.__secret,
            "units": self.__open_weather_unit[metric.value],
        }

        try:
            response = self.__client.get("/weather", params=query_params)
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            raise self.__handle_request_errors(location=location, exception=ex) from ex

        data = response.json()

        try:
            entitie = Weather(
                temperature=data["main"]["temp"],
                metric=metric.value,
                city=data["name"],
                country=data["sys"]["country"],
            )
        except KeyError as ex:
            self.__logger.critical(
                f"Unexpected response format, the expected key not exists in response: {ex}",
                exc_info=True,
            )
            raise UnexpectedClientError(
                client_name=self.__name, error_message=str(ex)
            ) from ex

        return entitie

    def __handle_request_errors(
        self, location: str, exception: httpx.HTTPStatusError
    ) -> NotFoundError | UnexpectedClientError:
        if exception.response.status_code == 404:
            message = f"{self.__name} - Not found weather to {location}"
            self.__logger.warn(message)
            formatted_exception = NotFoundError(
                resource_name=location,
                message=message,
                detail={
                    "location": location,
                    "original_error": exception.response.text,
                },
            )
            return formatted_exception

        if exception.response.status_code == 401:
            message = f"{self.__name} - Unauthorized search weather on provider"
            self.__logger.critical(message)
            formatted_exception = UnexpectedClientError(
                client_name=self.__name, error_message=message
            )
            return formatted_exception

        message = f"{self.__name} - Unexpected error {exception}"
        self.__logger.critical(message, exc_info=True)
        formatted_exception = UnexpectedClientError(
            client_name=self.__name,
            error_message=message,
            detail={
                "original_error": exception.response.text,
            },
        )

        return formatted_exception
