from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lang_pack.lang_ru import LANG_GENERAL
from models.album import Album
from models.artist import Artist
from models.release_types import get_release_type_value


class AlbumsCallbackFactory(CallbackData, prefix='album_id', sep=':'):
    album_id: str
    artist_id: str
    release_type: str


def create_albums_inline_kb(artist: Artist, albums: list[Album], release_type_key: str) -> InlineKeyboardMarkup:
    # Init keyboard instance
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Buttons list
    buttons: list[InlineKeyboardButton] = []

    # If result has more then 80 items, set link to website
    if len(albums) <= 80:
        from mediator.mediator import get_album_list_title
        for album in albums:
            title = get_album_list_title(album=album)
            factory = AlbumsCallbackFactory(album_id=album.id, artist_id=artist.id, release_type=release_type_key)
            buttons.append(
                InlineKeyboardButton(text=title, callback_data=factory.pack())
            )
    else:
        release_type = get_release_type_value(key=release_type_key)
        url = release_type['uri'].format(url=artist.link)
        text = LANG_GENERAL["See release_type on allmusic website"].format(release_type=release_type['label'])
        buttons.append(
            InlineKeyboardButton(text=text, url=url)
        )

    factory = AlbumsCallbackFactory(album_id='', artist_id=artist.id, release_type=release_type_key)
    buttons.append(
        InlineKeyboardButton(text="<< back", callback_data=factory.pack())
    )

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup()
