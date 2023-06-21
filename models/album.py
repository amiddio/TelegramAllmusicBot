from pydantic.dataclasses import dataclass
from models.model_general import ModelGeneral


@dataclass
class Album(ModelGeneral):
    """
    Модель альбома
    """

    id: str
    title: str
    year: str
    link: str
    cover: str
    label: str | None
    allmusic_rating: int | None
