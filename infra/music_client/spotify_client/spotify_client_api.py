import os

from typing import List

import httpx

from domain.enums.music_genre_type_enum import MusicGenreTypeEnum
from domain.shared.errors.forbidden_error import ForbiddenError
from domain.shared.errors.to_many_requests_error import ToManyRequestsError
from domain.shared.errors.unauthorized_error import UnauthorizedError

from domain.shared.errors.unexpected_client_error import UnexpectedClientError
from extensions.cache_extension import cache

from domain.entities.music import Music
from domain.interfaces.music_api_client import MusicApiClient
from extensions.log_extension import get_logger


class SpotifyClientApi(MusicApiClient):
    __name = "SpotifyClientApi"

    def __init__(self):
        self.__logger = get_logger(__name__)

        self.__client_id = os.getenv("SPOTIFY_API_ID")
        self.__client_secret = os.getenv("SPOTIFY_API_SECRET")
        self.__auth_api_url = os.getenv("SPOTIFY_AUTH_API_URL")
        self.__api_url = os.getenv("SPOTIFY_API_URL")

        self.__access_token_key = "access_token"

    def fetch_music_by_genre(self, genre: MusicGenreTypeEnum) -> List[Music]:

        access_token = self.__get_access_token()

        if access_token is None:
            self.__authorize()
            access_token = self.__get_access_token()

        headers = {"Authorization": f"Bearer {access_token}"}

        query_params = {
            "q": f"genre:{genre.value}",
            "type": "track",
            "limit": 10,
            "offset": 0,
        }

        try:
            response = httpx.get(
                f"{self.__api_url}/v1/search", params=query_params, headers=headers
            )
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            raise self.__handle_request_errors(exception=ex) from ex

        data = response.json()

        musics_list = []
        for item in data["tracks"]["items"]:
            name = item["name"]
            artist = item["artists"][0]["name"]

            music = Music(name=name, artist=artist)
            musics_list.append(music)

        return musics_list

    def __authorize(self):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        auth_client = httpx.Client(base_url=self.__auth_api_url, headers=headers)

        data = {
            "grant_type": "client_credentials",
            "client_id": self.__client_id,
            "client_secret": self.__client_secret,
        }

        try:
            response = auth_client.post("/api/token", data=data)
            response.raise_for_status()
        except httpx.HTTPStatusError as ex:
            raise self.__handle_request_errors(exception=ex) from ex

        data = response.json()

        access_token = data.get("access_token")
        expires_in = data.get("expires_in")

        self.__set_access_token(access_token=access_token, expires_in=expires_in)

    def __get_access_token(self) -> str | None:
        data = cache.get(self.__access_token_key)
        return data

    def __set_access_token(self, access_token: str, expires_in: int) -> None:
        cache.set(key=self.__access_token_key, value=access_token, timeout=expires_in)

    def __handle_request_errors(self, exception: httpx.HTTPStatusError) -> None:
        if exception.response.status_code == 401:
            message = f"{self.__name} - Unauthorized access on Spotify"
            self.__logger.critical(message)
            formatted_exception = UnauthorizedError(
                resource_name=self.__name,
                error_message=message,
                detail={"original_error": exception.response.text},
            )
            return formatted_exception

        if exception.response.status_code == 403:
            message = f"{self.__name} - Forbidden access on Spotify"
            self.__logger.critical(message)
            formatted_exception = ForbiddenError(
                resource_name=self.__name,
                error_message=message,
                detail={"original_error": exception.response.text},
            )
            return formatted_exception

        if exception.response.status_code == 429:
            message = f"{self.__name} - To many requests on Spotify, take a time"
            self.__logger.warn(message)
            formatted_exception = ToManyRequestsError(
                resource_name=self.__name,
                error_message=message,
                detail={"original_error": exception.response.text},
            )
            return formatted_exception
        else:
            message = f"{self.__name} - Unexpected error {exception}"
            self.__logger.critical(message, exc_info=True)
            formatted_exception = UnexpectedClientError(
                client_name=self.__name,
                error_message=message,
                detail={"original_error": exception.response.text},
            )
            return formatted_exception
