import re


class ModelGeneral:
    """
    Базовый кдасс для моделей
    """

    def __post_init__(self):
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                self.__dict__[key] = re.sub(r'\s+', r' ', value.strip())
