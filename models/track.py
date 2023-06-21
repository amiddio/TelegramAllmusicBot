from pydantic.dataclasses import dataclass
from models.model_general import ModelGeneral


@dataclass
class Track(ModelGeneral):
    """
    Модель песни альбома
    """

    number: str
    title: str
    composers: str
    performer: str
    time: str
