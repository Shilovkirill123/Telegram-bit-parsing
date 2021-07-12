import requests 
from bs4 import BeautifulSoup


def parsers(user_choice):

    r = requests.get("https://www.kinopoisk.ru/index.php?kp_query=" + user_choice)
    soup = BeautifulSoup(r.text, 'lxml')
    find_link =[]
    links = 'https://www.kinopoisk.ru/film/'

    for link in soup.find_all('p', class_='name'):
        for ids in link.find_all('a'):
            find_link.append(links + ids.get('data-id'))
    find_link = find_link[0]
    return find_link
 
