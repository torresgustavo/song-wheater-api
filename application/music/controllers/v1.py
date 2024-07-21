from flask import Response, json, request, Blueprint

from application.music.presenters.music_by_city_weather_presenter import (
    MusicBycityWeatherPresenter,
)
from domain.services.get_music_by_city_weather_service import (
    GetMusicByCityWeatherService,
)
from infra.music_client.spotify_client.spotify_client_api import SpotifyClientApi
from infra.weather_client.open_weather_api.open_weather_api_client import (
    OpenWeatherApiClient,
)

music_bp = Blueprint(name="Music", import_name=__name__, url_prefix="/v1/music")


@music_bp.get("/")
def search_music_by_city_weather() -> Response:
    city = request.args.get("city", type=str)

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
