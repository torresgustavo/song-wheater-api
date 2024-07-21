from abc import ABC, abstractmethod

from domain.entities.music import Music


class MusicApiClient(ABC):

    __name = None

    @abstractmethod
    def fetch_music_by_genre(self, genre: str) -> Music:
        raise NotImplementedError()
