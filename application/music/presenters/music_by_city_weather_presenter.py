from dataclasses import dataclass, field
from typing import List

from domain.entities.music import Music
from domain.entities.weather import Weather


@dataclass
class MusicPresenter:
    name: str
    artist: str

    @staticmethod
    def from_domain(music: Music) -> "MusicPresenter":
        return MusicPresenter(name=music.name, artist=music.artist)

    def to_dict(self) -> dict:
        return {"name": self.name, "artist": self.artist}


@dataclass
class MusicBycityWeatherPresenter:
    city: str
    temperature: float
    track_list: List[MusicPresenter] = field(default_factory=list)

    @staticmethod
    def from_domain(
        weather: Weather, music_list: List[Music]
    ) -> "MusicBycityWeatherPresenter":
        return MusicBycityWeatherPresenter(
            city=weather.city,
            temperature=weather.temperature,
            track_list=[MusicPresenter.from_domain(m) for m in music_list],
        )

    def to_dict(self) -> dict:
        return {
            "city": self.city,
            "temperature": self.temperature,
            "track_list": [m.to_dict() for m in self.track_list],
        }
