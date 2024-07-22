from flask import Response, json, request, Blueprint
from marshmallow import ValidationError

from application.music.presenters.music_by_city_weather_presenter import (
    MusicBycityWeatherPresenter,
)
from application.music.validators.search_music_validator import SearchMusicValidator

from domain.services.get_music_by_city_weather_service import (
    GetMusicByCityWeatherService,
)
from domain.shared.errors.base_error import BaseError

from infra.music_client.spotify_client.spotify_client_api import SpotifyClientApi
from infra.weather_client.open_weather_api.open_weather_api_client import (
    OpenWeatherApiClient,
)

music_bp = Blueprint(name="Music", import_name=__name__, url_prefix="/v1/music")


@music_bp.get("")
def search_music_by_city_weather() -> Response:
    city = request.args.get("city", type=str)
    city = SearchMusicValidator().load({"city": city})

    result = GetMusicByCityWeatherService(
        weather_client_api=OpenWeatherApiClient(),
        music_client_api=SpotifyClientApi(),
    ).execute(city=city)

    result = MusicBycityWeatherPresenter.from_domain(
        weather=result[0], music_list=result[1]
    )

    return Response(
        response=json.dumps(result.to_dict()),
        status=200,
        content_type="application/json",
        mimetype="application/json",
    )


@music_bp.errorhandler(ValidationError)
def handle_validation_error(error: ValidationError) -> Response:
    formatted_error = BaseError(
        message="Payload schema validation error",
        error_code="VALIDATION_ERROR",
        detail={"errors": error.messages},
    )

    return Response(
        response=json.dumps(formatted_error.to_dict()),
        status=400,
        content_type="application/json",
        mimetype="application/json",
    )
