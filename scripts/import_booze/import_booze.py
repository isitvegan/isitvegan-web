from bs4 import BeautifulSoup
import urllib.request


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


_BARNIVORE_URL = 'http://www.barnivore.com'


def _get_beer_soup(page):
    barnivore_beer_url = f'{_BARNIVORE_URL}/beer?page={page}'
    print(barnivore_beer_url)
    return _get_soup(barnivore_beer_url)


if __name__ == '__main__':
    soup = _get_beer_soup(1)
    products = soup.find(class_='products').find_all('li')
    for product in products:
        print(product.find(class_='info').get_text())
