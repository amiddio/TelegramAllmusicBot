from aiogram import Bot
from aiogram.types import BotCommand
from lang_pack.lang_ru import LANG_MENU


# Set menu button
async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command=command, description=description) for command, description in LANG_MENU.items()
    ]
    await bot.set_my_commands(main_menu_commands)
