import asyncio

from aiogram import Bot, Dispatcher
from config_data.config import load_config, Config
from handlers import user_handlers
from keyboards.set_menu import set_main_menu
from lang_pack.lang_ru import LANG_GENERAL
from logger.logger import log


async def main() -> None:

    # Load config data
    config: Config = load_config()

    # Init bot and dispatcher
    bot: Bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    # Add menu button
    await set_main_menu(bot)

    # Register routers in dispatcher
    dp.include_router(user_handlers.router)

    # Ignored some old updates and run polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print(LANG_GENERAL["Bot stopped!"])
        log().info(LANG_GENERAL["Bot stopped!"])
