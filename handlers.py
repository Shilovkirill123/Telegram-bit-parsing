from kino import general
from query import film_db
from search_film import parsers
from model import session


def talk_to_me(bot, update):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text('Напишите /1 и название фильма')


def film(bot, update):
    user_text = update.message.text
    user_text = user_text.split()
    del user_text[0]
    user_text = (' '.join(user_text))
    content = parsers(user_text)
    update.message.reply_text(content)
    print('Вывод фильма с кинопоиска')


def film_base(bot, update, user_data):
    user_text = update.message.text
    user_text = user_text.split()
    del user_text[0]
    user_text = (' '.join(user_text))
    a = film_db(user_text.capitalize())

    for film in a:
        update.message.reply_text(film)
        print('Вывод фильма с базы')
    if not a:
        print('В базе фильма нет')
        update.message.reply_text('В базе фильма нет, парсим...')
        print('Получение ссылки фильма')
        print(parsers(user_text))
        content = parsers(user_text)
        print('Парсим данные')
        attr_film = general(content)
        session.add(attr_film)
        session.commit()
        print('Запись данных в базу')
        update.message.reply_text(str(attr_film))
        print('Вывод фильма с базы')


    

