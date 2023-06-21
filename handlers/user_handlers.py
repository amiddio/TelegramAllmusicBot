import traceback

from aiogram import Router
from aiogram.filters import CommandStart, Command, Text
from aiogram.types import Message, CallbackQuery
from lang_pack.lang_ru import LANG_GENERAL
from logger.logger import log
from mediator.mediator import get_artists, get_artist_from_data, get_albums, get_artist_inline_kb, \
    get_album_from_data, get_album, get_album_back, get_artist_title

router: Router = Router()


# Catch the command '/start'
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LANG_GENERAL['/start'])


# Catch the command '/help'
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LANG_GENERAL['/help'])


# Handler for user search artist
@router.message()
async def proccess_search_artist(message: Message):
    try:
        artists = get_artists(message=message)
        for artist in artists:
            await message.answer(text=artist['title'], reply_markup=artist['callback_data'])
    except Exception as e:
        await message.answer(text=str(e))
        log().error(str(e))
        #traceback.print_exc()


# Handler for user clicked on inline button of artist release
@router.callback_query(Text(startswith='artist_id'))
async def process_artist_release_inline_button_press(callback: CallbackQuery):
    try:
        _, artist_id, release_type_key = callback.data.split(':')
        artist = get_artist_from_data(callback.from_user.id, artist_id)
        albums = get_albums(message=callback.message, artist=artist, release_type_key=release_type_key)
        await callback.message.edit_text(text=get_artist_title(artist=artist))
        await callback.message.edit_reply_markup(reply_markup=albums)
    except Exception as e:
        log().error(str(e))
        #traceback.print_exc()


# Handler for user clicked on album inline button
@router.callback_query(Text(startswith='album_id'))
async def process_album_inline_button_press(callback: CallbackQuery):
    try:
        _, album_id, artist_id, release_type_key = callback.data.split(':')
        if not album_id:
            artist = get_artist_from_data(callback.from_user.id, artist_id)
            await callback.message.edit_reply_markup(reply_markup=get_artist_inline_kb(artist))
        else:
            album = get_album_from_data(user_id=callback.message.from_user.id, artist_id=artist_id, album_id=album_id)
            if album:
                album_title = get_album(album=album)
                await callback.message.edit_text(text=album_title)
                await callback.message.edit_reply_markup(
                    reply_markup=get_album_back(artist_id=artist_id, release_type_key=release_type_key)
                )
    except Exception as e:
        log().error(str(e))
        #traceback.print_exc()



