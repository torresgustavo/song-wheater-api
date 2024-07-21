import os
from flask.testing import FlaskClient
from pytest_httpx import HTTPXMock


def test_search_music_by_city_weather_should_success(
    client: FlaskClient, httpx_mock: HTTPXMock
):
    # Arrange
    city_to_search = "test"
    expected_temperature = 25.01
    expected_genre_type = "pop"

    expected_artist = "artist"
    expected_music_name = "music"

    httpx_mock.add_response(
        method="GET",
        url=f"{os.getenv('WEATHER_API_URL')}/weather?q={city_to_search}&appid={os.getenv('WEATHER_API_SECRET')}&units=metric",
        json={
            "main": {"temp": expected_temperature},
            "name": city_to_search,
            "sys": {"country": "BR"},
        },
    )

    httpx_mock.add_response(
        method="POST",
        url=f"{os.getenv('SPOTIFY_AUTH_API_URL')}/api/token",
        json={
            "access_token": "test",
            "token_type": "Bearer",
            "expires_in": 3600,
        },
    )

    httpx_mock.add_response(
        method="GET",
        url=f"{os.getenv('SPOTIFY_API_URL')}/v1/search?q=genre:{expected_genre_type}&type=track&limit=10&offset=0",
        json={
            "tracks": {
                "items": [
                    {
                        "name": expected_music_name,
                        "artists": [{"name": expected_artist}],
                    }
                ]
            }
        },
    )

    # Act
    response = client.get(f"/v1/music?city={city_to_search}")

    # Assert
    assert response.status_code == 200

    response_data = response.json

    assert response_data["city"] == city_to_search
    assert response_data["temperature"] == expected_temperature
    assert response_data["track_list"][0]["artist"] == expected_artist
    assert response_data["track_list"][0]["name"] == expected_music_name
