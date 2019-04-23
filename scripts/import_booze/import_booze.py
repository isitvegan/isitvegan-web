from bs4 import BeautifulSoup
import urllib.request
import itertools
from collections import namedtuple


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


_BARNIVORE_URL = 'http://www.barnivore.com'


def _get_product_soup(product, page):
    product_url = f'{_BARNIVORE_URL}/{product}?page={page}'
    return _get_soup(product_url)


_ParsedProduct = namedtuple("_ParsedProduct", "status name url")


def _get_product_from_row(row_soup):
    status = row_soup.find(class_='status').get_text().strip()
    product_soup = row_soup.find(class_='info').find(class_='name')
    name = product_soup.get_text().strip()
    url = product_soup.a['href'].strip()

    return _ParsedProduct(status, name, url)


def _map_status(status):
    if status == 'Vegan Friendly':
        return 'vegan'
    if status == 'Not Vegan Friendly':
        return 'carnist'
    if status == 'Unknown':
        return 'itDepends'
    return None


def _parse_all_products(product):
    products = []
    for i in itertools.count(1):
        soup = _get_product_soup(product, i)
        products_soup = soup.find('ul', class_='products')
        if products_soup is None:
            break

        for product_row in products_soup.find_all('li'):
            parsed_product = _get_product_from_row(product_row)
            products.append(parsed_product)
    return products


def _print_all_products(product):
    products = _parse_all_products(product)
    for parsed_product in products:
        print('--')
        print(f'Status: {parsed_product.status}')
        print(f'Name: {parsed_product.name}')
        print(f'URL: {parsed_product.url}')


if __name__ == '__main__':
    _print_all_products('beer')
    _print_all_products('wine')
    _print_all_products('liquor')
