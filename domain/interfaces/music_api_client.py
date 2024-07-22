from abc import ABC, abstractmethod

from domain.entities.music import Music
from domain.enums.music_genre_type_enum import MusicGenreTypeEnum


class MusicApiClient(ABC):

    __name = None

    @abstractmethod
    def fetch_music_by_genre(self, genre: MusicGenreTypeEnum) -> Music:
        raise NotImplementedError()
