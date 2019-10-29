import urllib.request
from typing import List
import json
import base64
import os
from collections import namedtuple
from itertools import chain
import sys
import multiprocessing
import re
from datetime import datetime
import toml

_BEER_URL = 'http://barnivore.com/beer.json'
_WINE_URL = 'http://barnivore.com/wine.json'
_LIQOR_URL = 'http://barnivore.com/liquor.json'
_name_re = re.compile(r'[\(\)\-\t]')

_ParsedProduct = namedtuple("_ParsedProduct", "status name url")

def _company_url(company_id: str) -> str:
    return f'http://barnivore.com/company/{company_id}.json'

def _fetch_json(url: str):
    content = urllib.request.urlopen(url).read().decode()
    return json.loads(content)

def _fetch_json_cached(url: str):
    url_hash = base64.b64encode(url.encode('utf-8')).decode('utf-8')
    cache_file = os.path.join('.cache', f'request-{url_hash}.json')
    
    try:
        if os.path.exists(cache_file):
            return _read_json(cache_file)
        else:
            response = _fetch_json(url)
            _write_json(cache_file, response)
            return response
    except json.decoder.JSONDecodeError as error:
        raise Exception(f"error trying to decode response for {url} cache_file={cache_file}") from error

def _read_json(file_name: str):
    with open(file_name) as f:
        return json.load(f)

def _write_json(file_name: str, data):
    with open(file_name, 'w+') as f:
        json.dump(data, f)

def _fetch_company_ids(url: str) -> List[str]:
    companies = _fetch_json_cached(url)
    return [company['company']['id'] for company in companies]

def _fetch_company_products(company_id: str):
    response = _fetch_json_cached(_company_url(company_id))
    company = response['company']
    products = company['products']
    company_without_products = {key:company[key] for key in company if key != 'products'}
    return [{**product, 'company': company_without_products} for product in products]

def _fetch_companies() -> List[str]:
    beer = _fetch_company_ids(_BEER_URL)
    wine = _fetch_company_ids(_WINE_URL)
    liqor = _fetch_company_ids(_LIQOR_URL)
    return [*beer, *wine, *liqor]

def _fetch_products():
    companies = _fetch_companies()
    print(f'Fetching products for {len(companies)} companies...', file=sys.stderr)
    pool = multiprocessing.Pool()
    products_per_companies = pool.map(_fetch_company_products, companies, 5)
    return chain(*products_per_companies)

def _map_product(product) -> _ParsedProduct:
    name = product['product_name']
    state = product['status']
    product_id = product['id']
    url = f'http://www.barnivore.com/products/{product_id}'
    return _ParsedProduct(state, name, url)

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
    return ''


def _map_product_to_item(parsed_product):
    name = parsed_product.name
    state = _map_status_to_state(parsed_product.status)
    description = _map_description(state)
    url = parsed_product.url
    last_checked = datetime.utcnow().strftime('%Y-%m-%d')
    return {
        'name': name,
        'alternative_names': [],
        'state': state,
        'description': description,
        'sources': [
            { 'type': 'url', 'value': url, 'last_checked': last_checked },
        ],
        'vegan_alternatives': [],
    }

if __name__ == '__main__':
    products = [_map_product(product) for product in _fetch_products()]
    items = [_map_product_to_item(product) for product in products]
    print(toml.dumps({ 'items': items }))
