from pydantic import Field
from pydantic.dataclasses import dataclass
from models.model_general import ModelGeneral
from models.track import Track


@dataclass
class Disc(ModelGeneral):
    """
    Модель диска
    """

    title: str
    tracks: list[Track] = Field(default_factory=list)

    def append(self, track: Track) -> None:
        self.tracks.append(track)

