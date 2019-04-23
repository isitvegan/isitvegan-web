from bs4 import BeautifulSoup
import urllib.request
from itertools import count, chain
from collections import namedtuple
import re


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


_name_re = re.compile(r'[\(\)\-]')


def _map_name(name):
    ugly_name_result = _name_re.search(name)
    if ugly_name_result is not None:
        end_of_pretty_name = ugly_name_result.start()
        return name[:end_of_pretty_name].strip()

    return name


def _map_status_to_state(status):
    if status == 'Vegan Friendly':
        return 'vegan'
    if status == 'Not Vegan Friendly':
        return 'carnist'
    if status == 'Unknown':
        return 'itDepends'
    return None


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
    {{ type = "url", value = "{url}" }}
]
vegan_alternatives = []
    '''
    return item


def _import_all_products(product):
    items = []
    for page in count(1):
        soup = _get_product_soup(product, page)
        products_soup = soup.find('ul', class_='products')
        if products_soup is None:
            break

        for index, product_row in enumerate(products_soup.find_all('li')):
            parsed_product = _get_product_from_row(product_row)
            item = _map_product_to_item(parsed_product)
            items.append(item)
            print(
                f'Created {product} item #{page}.{index}: {parsed_product.name}')
            print(item)
    return items


_FILENAME = 'automatically_imported_booze.toml'


if __name__ == '__main__':
    items = []
    items.append(_import_all_products('beer'))
    items.append(_import_all_products('wine'))
    items.append(_import_all_products('liquor'))

    items = chain(*items)
    print(f'Finished creating items, writing them to {_FILENAME}')
    with open(_FILENAME, 'w') as import_file:
        for item in items:
            import_file.write(item)

    print('All done!')
