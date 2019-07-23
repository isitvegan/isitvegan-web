from bs4 import BeautifulSoup
import urllib.request
from itertools import count, chain
from collections import namedtuple
import re
from concurrent.futures import ThreadPoolExecutor, Future
from datetime import datetime


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


_BARNIVORE_URL = 'http://www.barnivore.com'


def _get_product_soup(product, group, page):
    product_url = f'{_BARNIVORE_URL}/{product}/{group}?page={page}'
    return _get_soup(product_url)


_ParsedProduct = namedtuple("_ParsedProduct", "status name url")


def _get_product_from_row(row_soup):
    status = row_soup.find(class_='status').get_text().strip()
    product_soup = row_soup.find(class_='info').find(class_='name')
    name = product_soup.get_text().strip()
    url = product_soup.a['href'].strip()

    return _ParsedProduct(status, name, url)


_name_re = re.compile(r'[\(\)\-\t]')


def _map_name(name):
    ugly_name_result = _name_re.search(name)
    if ugly_name_result is not None:
        end_of_pretty_name = ugly_name_result.start()
        name = name[:end_of_pretty_name]
    return name.replace('"', '\\"').strip()


def _map_status_to_state(status):
    status = status.lower()
    if status == 'vegan friendly':
        return 'vegan'
    if status == 'not vegan friendly':
        return 'carnist'
    if status == 'unknown':
        return 'itDepends'
    raise ValueError(f'Unexpected status: {status}')


def _map_description(status):
    if status == 'itDepends':
        return '''
Some variants of this item may contain animal products. 
Check the provided sources for further details.
'''
    return None


def _map_url(url):
    return _BARNIVORE_URL + url


def _map_product_to_item(parsed_product):
    name = _map_name(parsed_product.name)
    state = _map_status_to_state(parsed_product.status)
    description = _map_description(state)
    url = _map_url(parsed_product.url)
    last_checked = datetime.utcnow().strftime('%Y-%m-%d')
    item = f'''
[[items]]
name = "{name}"
alternative_names = []
state = "{state}"
description = '''
    if description is None:
        item += '""'
    else:
        item += f'"""{description}"""'
    item += f'''
sources = [
    {{ type = "url", value = "{url}", last_checked = "{last_checked}" }}
]
vegan_alternatives = []
'''
    return item


_GROUPS = [
    "0-9",
    "a-f",
    "g-l",
    "m-r",
    "s-t",
    "u-z"
]


def _import_all_products(product):
    items = []
    for group in _GROUPS:
        for page in count(1):
            soup = _get_product_soup(product, group, page)
            products_soup = soup.find('ul', class_='products')
            if products_soup is None:
                break

            for index, product_row in enumerate(products_soup.find_all('li')):
                parsed_product = _get_product_from_row(product_row)
                item = _map_product_to_item(parsed_product)
                items.append(item)
                print(
                    f'Created {group} {product} item #{page}.{index}: {parsed_product.name}')
    return items


_FILENAME = 'booze.toml'


if __name__ == '__main__':
    items = []
    worker_count = 2
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        futures = []

        print(f'Running worker #0 with the import of wine.')
        future = executor.submit(_import_all_products, 'wine')
        futures.append(future)

        print(f'Running worker #1 with the import of liquor.')
        future = executor.submit(_import_all_products, 'liquor')
        futures.append(future)

        print(f'Running main thread with the import of beer.')
        items = _import_all_products('beer')

        for future in futures:
            items.append(future.result())

    items = chain(*items)
    print(f'Finished creating items, writing them to {_FILENAME}')
    with open(_FILENAME, 'w') as import_file:
        for item in items:
            import_file.write(item)

    print('All done!')
