import requests
import settings
from fake_useragent import UserAgent

from bs4 import BeautifulSoup



def check_proxy():
    #good_proxy = []
    global proxies_list
    ua = UserAgent()
    if len(proxies_list) == 0:
        proxies_list = get_proxy()
    for proxy in get_proxy():
        headers = {'User-Agent': ua.random}
        proxies = {'http': proxy,
                'https': proxy
                }      
        try:
            result = requests.get('https://ya.ru/', headers=headers, proxies=proxies, timeout=1.5)
            result.raise_for_status()
            #good_proxy.append(proxy)
            print('Хороший прокси :)')
            #proxies_list = proxies_list[1:]
            print(len(proxies_list))
            return proxy
        
        
        except(requests.RequestException, ValueError, TimeoutError):
            print('Плохой прокси :(')
            print(proxies_list[0])
            proxies_list = proxies_list[1:]
            print(len(proxies_list))
    #print(good_proxy)        
    #return good_proxy

def get_html_proxy(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
          
    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
        return result.text    
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False



def get_proxy():
    link = 'https://getfreeproxylists.blogspot.com/'
    html = get_html_proxy(link)
    soup = BeautifulSoup(html, 'lxml')
    proxy = soup.find('div', class_="post-body entry-content")
    proxy = str(proxy).replace('<br/>', ' ').split()
    proxy = proxy[22:-4]
    #print(f'найденно проксей: {len(proxy)}')
    proxy = proxy[:300]
    #print(proxy)
    return proxy

proxies_list = get_proxy()


#check_proxy()


if __name__ == "__main__":
    pass