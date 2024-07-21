from flask import request, Blueprint
from infra.music_client.spotify_client.spotify_client_api import SpotifyClientApi

weather_bp = Blueprint(name="Weather", import_name=__name__, url_prefix="/v1/weather")


@weather_bp.get("/")
def search_music_by_city_wheater():
    city = request.args.get("city", type=str)
    SpotifyClientApi().fetch_music_by_genre("pop")
