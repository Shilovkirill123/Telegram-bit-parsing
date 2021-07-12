from model import session, Film
from search_film import parsers


def film_db(film_name):
    film_list_db = []
    for row in session.query(Film).filter(Film.name == film_name): 
        film_list_db.append(str(row))
    if not film_list_db:
        id_film = parsers(film_name).replace('https://www.kinopoisk.ru/film/', '')
        for row in session.query(Film).filter(Film.id_kinopoisk == id_film): 
            film_list_db.append(str(row))
    return film_list_db


