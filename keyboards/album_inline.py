from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.artists_inline import ArtistFilterByCallbackFactory
from lang_pack.lang_ru import LANG_GENERAL


def create_album_inline_kb(artist_id: str, release_type_key: str) -> InlineKeyboardMarkup:
    # Init keyboard instance
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Buttons list
    buttons: list[InlineKeyboardButton] = []

    factory = ArtistFilterByCallbackFactory(artist_id=artist_id, release_type=release_type_key)
    buttons.append(
        InlineKeyboardButton(text=LANG_GENERAL['back'], callback_data=factory.pack())
    )

    kb_builder.row(*buttons, width=1)

    return kb_builder.as_markup()
