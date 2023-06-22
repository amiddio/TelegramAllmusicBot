LANG_MENU: dict[str, str] = {
    '/start': "Запускаем бот",
    '/help': "Помощь",
}

LANG_GENERAL: dict[str, str] = {
    "/start": "Бот парсит ресурс Allmusic, и предоставляет поиск и просмотр исполнителей и их дискографии.\n"
              "Укажите в запросе исполнителя и следуя навигации просматривайте дискографию",
    "/help": "- укажите в запросе исполнителя\n"
             "- следуя навигации просматривайте его дискографию",
    "Bot stopped!": "Бот остановлен!",
    "Artist": "<b>{artist}</b>",
    "Genres": "Жанры: {genres}",
    "Decades": "Декады: {decades}",
    "bold": "<b>{content}</b>",
    "Year": "Год: {year}",
    "Label": "Лэйбл: {label}",
    "Allmusic rating": "Allmusic рейтинг: {rating}",
    "Composers": "Автор(ы)",
    "Performer": "Исполнители",
    "back": "<< назад",
    "See release_type on allmusic website": "Смотрите {release_type} на allmusic сайте"
}

LANG_ERR: dict[str, str] = {
    "Artist not found": "Такой исполнитель не найден"
}
