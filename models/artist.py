from pydantic.dataclasses import dataclass
from models.model_general import ModelGeneral


@dataclass
class Artist(ModelGeneral):
    """
    Модель исполнителя
    """

    id: str
    name: str
    link: str
    genres: str | None
    decades: str | None
