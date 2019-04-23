from bs4 import BeautifulSoup
import urllib.request
import itertools


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


_BARNIVORE_URL = 'http://www.barnivore.com'


def _get_product_soup(product, page):
    product_url = f'{_BARNIVORE_URL}/{product}?page={page}'
    return _get_soup(product_url)


def _print_all_products(product):
    for i in itertools.count(1):
        soup = _get_product_soup(product, i)
        products = soup.find('ul', class_='products')
        if products is None:
            break

        for product_row in products.find_all('li'):
            status = product_row.find(class_='status').get_text().strip()
            product_soup = product_row.find(class_='info').find(class_='name')
            product_name = product_soup.get_text().strip()
            product_url = product_soup.a['href'].strip()
            print('---')
            print(f'Status: {status}')
            print(f'Name: {product_name}')
            print(f'URL: {product_url}')


if __name__ == '__main__':
    _print_all_products('beer')
    _print_all_products('wine')
    _print_all_products('liquor')
