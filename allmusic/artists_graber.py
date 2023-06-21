import json

from bs4 import NavigableString, Tag
from allmusic.allmusic_base import AllmusicBase
from models.artist import Artist


class ArtistsGraber(AllmusicBase):
    """
    Класс ищет исполнителей и собирает информацию о найденных
    """

    __ARTIST_URL = 'https://www.allmusic.com/search/artists/{artist}'

    def find(self, qw: str) -> list[Artist]:
        url = ArtistsGraber.__ARTIST_URL.format(artist=qw)
        result = []
        soup = self.get_html_parser_soup(url=url)
        content = soup.find('div', class_='results')
        if not content:
            return result

        content = content.ul.children
        for indx, li in enumerate(content, start=1):
            # Ignored more then 10 items
            if indx > 10:
                break
            if isinstance(li, NavigableString):
                continue
            artist_name, artist_link, artist_id = self._get_block_name(li)
            # Looking for an exact artist match
            if artist_name.lower() != qw.lower():
                continue
            result.append(
                Artist(id=artist_id, name=artist_name, link=artist_link,
                       genres=self._get_block_genres(content=li),
                       decades=self._get_block_decades(content=li)
                       )
            )
        return result

    def _get_block_name(self, content: Tag) -> tuple | None:
        block_name = content.find('div', class_='name').find('a')
        if block_name:
            artist_name = block_name.text
            artist_link = block_name['href']
            artist_id = json.loads(block_name['data-tooltip'])['id']
            return artist_name, artist_link, artist_id
        return

    def _get_block_genres(self, content: Tag) -> str | None:
        res = content.find('div', class_='genres')
        if res:
            return res.text

    def _get_block_decades(self, content: Tag) -> str | None:
        res = content.find('div', class_='decades')
        if res:
            return res.text


if __name__ == '__main__':
    #r = ArtistsGraber().find(qw='1')
    #print(r)
    pass
