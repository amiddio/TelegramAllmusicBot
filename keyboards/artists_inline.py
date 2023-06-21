from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from allmusic.discography_filter_check_graber import DiscographyFilterCheckGraber
from models.artist import Artist
from models.release_types import get_release_type_value


class ArtistFilterByCallbackFactory(CallbackData, prefix='artist_id', sep=':'):
    artist_id: str
    release_type: str


def create_artists_inline_kb(artist: Artist) -> InlineKeyboardMarkup | None:

    # Init keyboard instance
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Buttons list
    buttons: list[InlineKeyboardButton] = []

    release_types = DiscographyFilterCheckGraber().grab(url=artist.link)
    if not release_types:
        return

    for release_type_key in release_types:
        release_type = get_release_type_value(key=release_type_key)

        factory = ArtistFilterByCallbackFactory(artist_id=artist.id, release_type=release_type_key)
        buttons.append(
            InlineKeyboardButton(text=release_type['label'], callback_data=factory.pack())
        )

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup()
