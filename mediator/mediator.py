from aiogram.types import Message, InlineKeyboardMarkup
from typing_extensions import Type
from collections import defaultdict
from allmusic.album_graber import AlbumGraber
from allmusic.artists_graber import ArtistsGraber
from allmusic.discography_graber import DiscographyGraber
from keyboards.album_inline import create_album_inline_kb
from keyboards.albums_inline import create_albums_inline_kb
from keyboards.artists_inline import create_artists_inline_kb
from lang_pack.lang_ru import LANG_ERR, LANG_GENERAL
from logger.logger import log
from models.album import Album
from models.artist import Artist
from models.disc import Disc
from models.release_types import get_release_type_value

user_data_artists: defaultdict[int, list[Type[Artist]]] = defaultdict(list)
user_data_albums: defaultdict[int, dict[str, list[Type[Album]]]] = defaultdict(dict)


def get_artists(message: Message) -> list:
    """
    Функция возвращает исполнителя с инлайн кнопками его релизов
    :param message: Message
    :return: list
    """
    artist = message.text.lower().strip()

    artists: list[Artist] = ArtistsGraber().find(artist)
    # Artist(s) not found
    if not artists:
        log().error(LANG_ERR['Artist not found'])
        raise ValueError(LANG_ERR['Artist not found'])

    result: list[dict[str, InlineKeyboardMarkup]] = []
    for item in artists:
        # Save artist to temporary dict
        user_data_artists[message.from_user.id].append(item)
        result.append({
            'title': get_artist_title(artist=item),
            'callback_data': get_artist_inline_kb(artist=item)
        })
        log().info(f"User '{message.from_user.id}:{message.from_user.full_name}' searched '{item.name}'")

    return result


def get_albums(message: Message, artist: Artist, release_type_key: str) -> InlineKeyboardMarkup:
    """
    Функция возвращает список инлайн кнопок альбомов
    :param message: Message
    :param artist: Artist
    :param release_type_key:
    :return: str
    """
    key = ':'.join([artist.id, release_type_key])
    release_type = get_release_type_value(key=release_type_key)

    if not user_data_albums[message.from_user.id].get(artist.id, None):
        url = release_type['uri'].format(url=artist.link)
        albums = DiscographyGraber().grab(url=url)
        user_data_albums[message.from_user.id][key] = albums
    else:
        albums = user_data_albums[message.from_user.id][key]

    return create_albums_inline_kb(artist=artist, albums=albums, release_type_key=release_type_key)


def get_album(album: Album) -> str:
    """
    Функция возвращает альбом с списком песен и обложкой
    :param album: Album
    :return: str
    """
    discs = AlbumGraber().grab(url=album.link)
    album_title = get_album_detail_title(album=album)
    album_tracks = get_album_tracking_listing(discs=discs)
    return album_title + album_tracks + f"\n{album.cover}"


def get_album_back(artist_id: str, release_type_key: str) -> InlineKeyboardMarkup:
    """
    Возвращается инлайн кнопка "назад" на странице альбома
    :param artist_id: str
    :param release_type_key: str
    :return: InlineKeyboardMarkup
    """
    return create_album_inline_kb(artist_id=artist_id, release_type_key=release_type_key)


def get_artist_inline_kb(artist: Artist) -> InlineKeyboardMarkup:
    """
    Возвращается список инлайн кнопок релизов исполнителя
    :param artist: Artist
    :return: InlineKeyboardMarkup
    """
    return create_artists_inline_kb(artist=artist)


def get_artist_from_data(user_id: int, artist_id: str) -> Artist | None:
    """
    Возвращает исполнителя из массива пользовательских данных
    :param user_id: int
    :param artist_id: str
    :return: Artist | None
    """
    for key, value in user_data_artists.items():
        if key == user_id:
            for artist in value:
                if artist.id == artist_id:
                    return artist


def get_album_from_data(user_id: int, artist_id: str, album_id: str) -> Album | None:
    """
    Возвращает альбом из массива пользовательских данных
    :param user_id: int
    :param artist_id: str
    :param album_id: str
    :return: Album | None
    """
    user_data = user_data_albums.get(user_id, None)
    if user_data:
        for key, value in user_data.items():
            art_id = key.split(':')[0]
            if art_id == artist_id:
                for item in value:
                    if album_id == item.id:
                        return item


def get_artist_title(artist: Artist) -> str:
    """
    Функция возвращает форматированую секцию исполнителя
    :param artist: Artist
    :return: str
    """
    result = []
    if artist.name:
        result.append(LANG_GENERAL['Artist'].format(artist=artist.name))
    if artist.genres:
        result.append(LANG_GENERAL['Genres'].format(genres=artist.genres))
    if artist.decades:
        result.append(LANG_GENERAL['Decades'].format(decades=artist.decades))
    return '\n'.join(result)


def get_album_list_title(album: Album) -> str:
    """
    Функция возвращает форматированую секцию альбома в списке инлайн кнопок
    :param album: Album
    :return: str
    """
    result = []
    if album.year:
        result.append(album.year)
    if album.title:
        rating = ''
        if album.allmusic_rating:
            rating = f" ({album.allmusic_rating})"
        result.append(album.title + rating)

    return ' - '.join(result)


def get_album_detail_title(album: Album) -> str:
    """
    Функция возвращает форматированую секцию название альбома при отображении списка песен
    :param album: Album
    :return: str
    """
    result = []
    if album.title:
        result.append(LANG_GENERAL["bold"].format(content=album.title))
    if album.year:
        result.append(LANG_GENERAL['Year'].format(year=album.year))
    if album.label:
        result.append(LANG_GENERAL['Label'].format(label=album.label))
    if album.allmusic_rating:
        result.append(LANG_GENERAL['Allmusic rating'].format(rating=album.allmusic_rating))
    return '\n'.join(result) + '\n'


def get_album_tracking_listing(discs: list[Disc]) -> str:
    """
    Функция возвращает список треков
    :param discs: list[Disc]
    :return: str
    """
    result = []
    for disc in discs:
        result.append(f"\n{LANG_GENERAL['bold'].format(content=disc.title)}\n")
        for track in disc.tracks:
            track_time = track_composers = ''
            if track.time:
                track_time = f"({track.time})"
            if track.composers:
                track_composers = f"{LANG_GENERAL['Composers']}: <i>{track.composers}</i>\n"
            # if track.performer:
            #     track_performer = f"{LANG_GENERAL['Performer']}: {track.performer}"
            track_title = f"{track.number}. <u>{track.title}</u> {track_time}\n"
            result.append(''.join([track_title, track_composers]))
    return ''.join(result)
