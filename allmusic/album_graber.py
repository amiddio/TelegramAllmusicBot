from bs4 import NavigableString
from allmusic.allmusic_base import AllmusicBase
from models.disc import Disc
from models.track import Track


class AlbumGraber(AllmusicBase):
    """
    Класс собирает информацию об альбоме: номер трека, название трека, время и т.д.
    """

    def grab(self, url: str) -> list[Disc]:
        soup = self.get_html_parser_soup(url=url)
        track_listing = soup.find_all("div", class_="disc")
        result = []
        for item in track_listing:
            if isinstance(item, NavigableString):
                continue
            disc = Disc(title=self._get_disc_title(disc=item))

            track_tables = item.find_all('table')
            for track_table in track_tables:
                for track in track_table.find('tbody').children:
                    if isinstance(track, NavigableString):
                        continue
                    disc.append(
                        Track(
                            number=self._get_track_number(track),
                            title=self._get_track_title(track),
                            composers=self._get_track_composers(track),
                            performer=self._get_track_performer(track),
                            time=self._get_track_time(track)
                        )
                    )
            result.append(disc)
        return result

    def _get_disc_title(self, disc) -> str:
        return disc.find('h3').text

    def _get_track_number(self, track) -> str:
        return track.find('td', class_='tracknum').text

    def _get_track_title(self, track) -> str:
        return track.find('div', class_='title').a.text

    def _get_track_composers(self, track) -> str:
        composers = track.find('div', class_='composer').children
        result = []
        for composer in composers:
            result.append(composer.text)
        return ' '.join(result)

    def _get_track_performer(self, track) -> str:
        result = []
        performer_primary = track.find('span', class_='primary')
        if performer_primary:
            result.append(performer_primary.text)
        performer_featuring = track.find('span', class_='featuring')
        if performer_featuring:
            result.append(performer_featuring.text)
        return ' '.join(result)

    def _get_track_time(self, track) -> str:
        return track.find('td', class_='time').text


if __name__ == '__main__':
    pass
