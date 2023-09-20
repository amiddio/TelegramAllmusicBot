from bs4 import NavigableString
from allmusic.allmusic_base import AllmusicBase
from models.release_types import get_release_type_key


class DiscographyFilterCheckGraber(AllmusicBase):
    """
    Класс определяет какие релизы есть у исполнителя.
    Например, это могут быть альбомы, синглы, компиляции и т.д.
    """

    __DISGORRAPHY_URL = '{url}/discography'

    def grab(self, url: str) -> list[str] | None:
        url = DiscographyFilterCheckGraber.__DISGORRAPHY_URL.format(url=url)
        soup = self.get_html_parser_soup(url=url)

        discography_table = soup.find("nav", class_="release-types")

        if discography_table:
            result = discography_table.select('label')
        else:
            return

        release_types = []
        for tp in result:
            if isinstance(tp, NavigableString):
                continue
            r = tp.find('a').text
            if r.lower() == 'all':
                continue
            release_types.append(get_release_type_key(label=r))
        return release_types


if __name__ == '__main__':
    pass
