import json
import re

from bs4 import NavigableString, Tag
from allmusic.allmusic_base import AllmusicBase
from models.album import Album


class DiscographyGraber(AllmusicBase):
    """
    Класс собирает информацию об альбомах
    """

    def grab(self, url: str) -> list[Album]:

        soup = self.get_html_parser_soup(url=url)
        discography_table = soup.find("section", class_="discography").table.tbody.children
        result = []
        for tr in discography_table:
            if isinstance(tr, NavigableString):
                continue
            result.append(
                Album(
                    id=self._get_album_id(tr),
                    title=self._get_album_title(tr),
                    year=self._get_album_year(tr),
                    link=self._get_album_link(tr),
                    cover=self._get_album_cover(tr),
                    label=self._get_album_label(tr),
                    allmusic_rating=self._get_album_allmusic_rating(tr)
                )
            )
        return result

    def _get_album_id(self, content: Tag) -> str:
        return json.loads(content.find('td', class_='title').a['data-tooltip'])['id']

    def _get_album_title(self, content: Tag) -> str:
        return content.find('td', class_='title')['data-sort-value']

    def _get_album_year(self, content: Tag) -> str:
        res = content.find('td', class_='year')
        if res:
            return res.text

    def _get_album_cover(self, content: Tag) -> str:
        return content.find('img', class_='cropped-image')['src']

    def _get_album_link(self, content: Tag) -> str:
        return content.find('td', class_='title').find('a')['href']

    def _get_album_label(self, content: Tag) -> str:
        res = content.find('td', class_='label').find('a')
        if res:
            return res.text

    def _get_album_allmusic_rating(self, content: Tag) -> int | None:
        rating_allmusic = content.find('td', class_='all-rating')['data-sort-value']
        if rating_allmusic:
            return int(re.search(r'(\d+)', rating_allmusic).group())
        return


if __name__ == '__main__':
    pass
