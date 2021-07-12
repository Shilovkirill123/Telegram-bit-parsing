import requests
import settings
from fake_useragent import UserAgent

from model import Film
from bs4 import BeautifulSoup
from search_film import parsers
from get_proxy import check_proxy


def get_html(url):
    film_list = None
    while film_list is None:
        ua = UserAgent()
        headers = {'User-Agent': ua.random,
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                    }

        proxy =  check_proxy()

        proxies = {'http': proxy,
                'https': proxy
                }
        
        try:
            result = requests.get(url, headers=headers, proxies=proxies, timeout=7 )
            result.raise_for_status()
            #print(result.text)
            result = result.text
            soup = BeautifulSoup(result, 'html.parser')
            film_list = soup.find('span', class_="moviename-title-wrapper").text
            print(film_list)
            return result

        except(requests.RequestException, ValueError):
            print('Не удалось подключиться, ищем дальше...')
            #return False
            continue
        except:
            print('Капча, поиск другой прокси...')
            continue


def get_name_film(soup):
    film_list = soup.find('span', class_="moviename-title-wrapper").text
    return film_list
    


def get_film(soup):
    attr = ['год', 'страна', 'режиссер', 'сценарий', 'продюсер', 'оператор',
            'композитор', 'художник', 'монтаж', 'бюджет', 'маркетинг',
            'сборы в США', 'сборы в мире', 'премьера (мир)', 'премьера (РФ)']
    film_attr = {}
    film_lists = soup.find('table', {'class': 'info'}).find_all('tr')
    for film in film_lists:
        a = film.find('td', {'class': 'type'}).text
        try:
            if a in attr:
                film_attr[a.capitalize()] = film.find("a").text
        except(AttributeError):
            film_attr[a.capitalize()] = 'нет данных'
    return film_attr


def get_genre_film(soup):
    genres_0 = []
    genres = []
    film_lists = soup.find('table', {'class': 'info'}).find_all('tr')
    for film in film_lists:
        a = film.find('td', {'class': 'type'}).text
        if a == 'жанр':
            for genre in film:
                genres_0.append(genre.find_all('a'))
            genres_0 = genres_0[1]
            for b in genres_0:
                genres.append(b.text)
    del genres[-1]
    for gen in genres:
        gen = ', '.join(genres)
    return gen


def get_tagline_film(soup):
    film_lists = soup.find('table', {'class': 'info'}).find_all('tr')
    for film in film_lists:
        a= film.find('td', {'class': 'type'}).text
        if a == 'слоган':
            tagline = film.find('td', {'style': 'color: #555'}).text
    return tagline


def get_duration_film(soup):
    film_list = soup.find('table', {'class': 'info'}).find('td', {'class': 'time'}).text
    return film_list


def get_actors_film(soup):
    actors = []
    film_list = soup.find_all('li', {'itemprop': 'actors'})
    for actor in film_list:
        actors.append(actor.text)
        actor = ', '.join(actors[:4])
    return actor


def get_rating_film(soup):
    try:
        film_list = soup.find('span', {'class': 'rating_ball'}).text
        return film_list
    except(AttributeError):
        film_list = '-'
        return film_list



def get_imdb_film(soup):
    try:
        film_list = soup.find('div', {'style': 'color:#999;font:100 11px tahoma, verdana'}).text.split()
        film_list = film_list[1]
        return film_list
    except(AttributeError):
        film_list = '-'
        return film_list


def general(link):
    html = get_html(link)
    soup = BeautifulSoup(html, 'html.parser')
    film_data = {}
    film_data['Название фильма'] = get_name_film(soup)
    film_data['Слоган'] = get_tagline_film(soup)
    film_data['Актеры'] = get_actors_film(soup)
    film_data['Жанр'] = get_genre_film(soup)
    film_data['Рейтинг Кинопоиска'] = get_rating_film(soup)
    film_data['Рейтинг IMDB'] = get_imdb_film(soup)
    for a in get_film(soup):
        film_data[a] = get_film(soup)[a]
    film_data['Продолжительность'] = get_duration_film(soup)
    film_data['Номер на кинопоиске'] = link.replace('https://www.kinopoisk.ru/film/', '')
    film = Film(
        id_kinopoisk=film_data['Номер на кинопоиске'], name=get_name_film(soup), tagline=get_tagline_film(soup),
        genre=get_genre_film(soup), actors=get_actors_film(soup), director=film_data['Режиссер'], rating=get_rating_film(soup),
        rating_imdb=get_imdb_film(soup), year=film_data['Год']
    )
    return film
