#!/usr/bin/env python3

from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.request
import requests
import re
import os
from itertools import islice
from concurrent.futures import ThreadPoolExecutor, Future
import multiprocessing

VEGAN_E_NUMBERS = [
    "E133",
    "E140",
    "E141",
    "E142",
    "E143",
    "E150a",
    "E150b",
    "E150c",
    "E150d",
    "E151",
    "E152",
    "E154",
    "E155",
    "E160a",
    "E160b",
    "E160c",
    "E160d",
    "E160e",
    "E160f",
    "E161a",
    "E161b",
    "E161c",
    "E161d",
    "E161e",
    "E161f",
    "E162",
    "E163",
    "E170",
    "E171",
    "E172",
    "E173",
    "E174",
    "E175",
    "E180",
    "E181",

    "E200",
    "E201",
    "E202",
    "E203",
    "E210",
    "E211",
    "E212",
    "E213",
    "E214",
    "E215",
    "E216",
    "E217",
    "E218",
    "E219",
    "E220",
    "E221",
    "E222",
    "E223",
    "E224",
    "E225",
    "E226",
    "E227",
    "E228",
    "E230",
    "E231",
    "E232",
    "E233",
    "E234",
    "E235",
    "E236",
    "E237",
    "E238",
    "E239",
    "E240",
    "E242",
    "E249",
    "E250",
    "E251",
    "E260",
    "E261",
    "E262",
    "E263",
    "E264",
    "E280",
    "E281",
    "E282",
    "E283",
    "E284",
    "E285",
    "E290",
    "E296",
    "E297",

    "E300",
    "E301",
    "E302",
    "E303",
    "E304",
    "E306",
    "E307",
    "E308",
    "E309",
    "E310",
    "E311",
    "E312",
    "E315",
    "E316",
    "E317",
    "E318",
    "E319",
    "E320",
    "E321",
    "E329",
    "E330",
    "E331",
    "E332",
    "E333",
    "E334",
    "E335",
    "E336",
    "E337",
    "E338",
    "E339",
    "E340",
    "E341",
    "E343",
    "E350",
    "E351",
    "E352",
    "E353",
    "E354",
    "E355",
    "E356",
    "E357",
    "E363",
    "E365",
    "E366",
    "E367",
    "E370",
    "E375",
    "E380",
    "E381",
    "E385",
    "E400",
    "E401",
    "E402",
    "E403",
    "E404",
    "E405",
    "E406",
    "E407",
    "E407a",
    "E410",
    "E412",
    "E413",
    "E414",
    "E415",
    "E416",
    "E417",
    "E418",
    "E420",
    "E421",
    "E425",
    "E440",
    "E444",
    "E445",
    "E450",
    "E451",
    "E452",
    "E459",
    "E460",
    "E461",
    "E462",
    "E463",
    "E464",
    "E465",
    "E466",
    "E468",
    "E469",

    "E500",
    "E501",
    "E503",
    "E504",
    "E507",
    "E508",
    "E509",
    "E510",
    "E511",
    "E512",
    "E513",
    "E517",
    "E518",
    "E519",
    "E520",
    "E521",
    "E522",
    "E523",
    "E524",
    "E525",
    "E526",
    "E527",
    "E528",
    "E529",
    "E530",
    "E535",
    "E536",
    "E538",
    "E540",
    "E541",
    "E543",
    "E544",
    "E545",
    "E550",
    "E551",
    "E552",
    "E553b",
    "E554",
    "E555",
    "E556",
    "E558",
    "E559",
    "E574",
    "E575",
    "E576",
    "E577",
    "E578",
    "E579",

    "E620",
    "E621",
    "E622",
    "E623",
    "E624",
    "E625",
    "E626",
    "E628",
    "E629",
    "E630",
    "E632",
    "E633",
    "E634",
    "E636",
    "E637",

    "E900",
    "E902",
    "E903",
    "E905",
    "E905a",
    "E905b",
    "E905c",
    "E906",
    "E907",
    "E908",
    "E912",
    "E914",
    "E915",
    "E922",
    "E923",
    "E924",
    "E925",
    "E926",
    "E927",
    "E297b",
    "E928",
    "E930",
    "E938",
    "E939",
    "E940",
    "E941",
    "E942",
    "E943a",
    "E943b",
    "E944",
    "E948",
    "E949",
    "E950",
    "E951",
    "E952",
    "E953",
    "E954",
    "E955",
    "E957",
    "E959",
    "E965",
    "E967",
    "E999",

    "E1103",
    "E1105",
    # The following don't seem to exist
    # "E1106",
    # "E1107",
    # "E1108",
    # "E1109",
    # "E1110",
    # "E1111",
    # "E1112",
    # "E1113",
    # "E1114",
    # "E1115",
    # "E1116",
    # "E1117",
    # "E1118",
    # "E1119",
    # "E1120",
    # "E1121",
    # "E1122",
    # "E1123",
    # "E1124",
    # "E1125",
    # "E1126",
    # "E1127",
    # "E1128",
    # "E1129",
    # "E1130",
    # "E1131",
    # "E1132",
    # "E1133",
    # "E1134",
    # "E1135",
    # "E1136",
    # "E1137",
    # "E1138",
    # "E1139",
    # "E1140",
    # "E1141",
    # "E1142",
    # "E1143",
    # "E1144",
    # "E1145",
    # "E1146",
    # "E1147",
    # "E1148",
    # "E1149",
    # "E1150",
    # "E1151",
    # "E1152",
    # "E1153",
    # "E1154",
    # "E1155",
    # "E1156",
    # "E1157",
    # "E1158",
    # "E1159",
    # "E1160",
    # "E1161",
    # "E1162",
    # "E1163",
    # "E1164",
    # "E1165",
    # "E1166",
    # "E1167",
    # "E1168",
    # "E1169",
    # "E1170",
    # "E1171",
    # "E1172",
    # "E1173",
    # "E1174",
    # "E1175",
    # "E1176",
    # "E1177",
    # "E1178",
    # "E1179",
    # "E1180",
    # "E1181",
    # "E1182",
    # "E1183",
    # "E1184",
    # "E1185",
    # "E1186",
    # "E1187",
    # "E1188",
    # "E1189",
    # "E1190",
    # "E1191",
    # "E1192",
    # "E1193",
    # "E1194",
    # "E1195",
    # "E1196",
    # "E1197",
    # "E1198",
    # "E1199",
    "E1200",
    "E1201",
    "E1202",
    "E1400",
    "E1401",
    "E1402",
    "E1403",
    "E1404",
    "E1410",
    "E1412",
    "E1413",
    "E1414",
    "E1420",
    "E1421",
    "E1422",
    "E1430",
    "E1440",
    "E1441",
    "E1442",
    "E1450",
    "E1451",
    "E1505",
    "E1510",
    "E1518",
    "E1520",
]

_E_NUMBERS_URL = 'https://en.wikipedia.org/wiki/E_number'


def _get_wikipedia_e_number_and_title_table_data(e_numbers_soup, e_number):
    e_number_table_data = None

    for table in e_numbers_soup.find_all('table'):
        table_body = table.find('tbody')
        for table_row in table_body.find_all('tr'):
            for table_data in table_row.find_all('td'):
                text = table_data.get_text().strip()
                if text == e_number:
                    e_number_table_data = table_data
                elif e_number_table_data is not None:
                    # We're in the title table data
                    return e_number_table_data, table_data
    raise ValueError(
        f'{e_number} was not found on Wikipedia page {_E_NUMBERS_URL}')


def _get_url(soup):
    anchor = soup.a
    if anchor is None:
        return None
    return anchor['href']


def _get_wikipedia_article_url(article):
    return f'https://en.wikipedia.org/wiki/{article}'


def _does_article_exist(url):
    return url.find('redlink=1') == -1


def _get_wikipedia_url(e_number_soup, title_soup):
    possible_urls = [_get_url(e_number_soup), _get_url(title_soup)]

    for url_fragment in possible_urls:
        if url_fragment is not None:
            article = url_fragment.replace('/wiki/', '')
            url = _get_wikipedia_article_url(article)
            if _does_article_exist(url):
                return url

    return _E_NUMBERS_URL


_title_re = re.compile(r'[\(\)\:]')


def _get_e_number_title(title_soup):
    title = title_soup.get_text().strip()

    ugly_title_result = _title_re.search(title)
    if ugly_title_result is not None:
        end_of_pretty_title = ugly_title_result.start()
        return title[:end_of_pretty_title].strip()

    return title


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


def _contains_e_number(text, e_number):
    for e_number_variation in _get_e_number_variations(e_number):
        if e_number_variation in text:
            return True
    return False


def _contains_the_word_e_number(text):
    e_number = 'E Number'
    e_number_variations = [e_number, e_number.lower(), e_number.replace(
        'E', 'e'), e_number.replace('N', 'n')]
    for e_number_variation in e_number_variations:
        if e_number_variation in text:
            return True
    return False


def _get_uk_food_guide_url(e_number):
    e_number = e_number.lower()
    url = f'http://www.ukfoodguide.net/{e_number}.htm'
    status_code = requests.head(url).status_code
    if status_code is 200:
        return url
    else:
        return None


_italic_re = re.compile(r'</?i>')
_a_re = re.compile(r'</?a( href=".*")?( title=".*")?>')

_non_dot_re = re.compile(r'\n([^•])')
_dot_re = re.compile(r'\s*•')

_non_semicolon_re = re.compile(r'\n([^;])')
_semicolon_re = re.compile(r'\s*;')

_comma_space_re = re.compile(r'\s*, ')

_e_number_re = re.compile(r'\b[Ee] *\d+\w*')


def _get_alternative_names(article_soup, e_number):
    info_box = article_soup.find(class_='infobox bordered')
    if info_box is None:
        return []
    for row in info_box.find_all('tr'):
        for data in row.find_all('td'):
            text = data.get_text()
            ALTERNATIVE_NAMES_IDENTIFIER = "Other names"
            if ALTERNATIVE_NAMES_IDENTIFIER in text:
                # I hate Wikipedia's 'Other names' section
                # It's so hecking inconsistent!
                html = str(data)
                html = _italic_re.sub('', html)
                html = _a_re.sub('', html)

                data = BeautifulSoup(html, 'html.parser')

                name_list = data.get_text("\n")
                names = name_list.replace(ALTERNATIVE_NAMES_IDENTIFIER, '')
                names = names.strip()
                names = names.replace('\n ', ' ')
                names = names.strip()
                if '•' in names:
                    names = _non_dot_re.sub(r'\1', names)
                    names = _dot_re.sub('\n', names)
                elif ';' in names:
                    names = _non_semicolon_re.sub(r'\1', names)
                    names = _semicolon_re.sub('\n', names)
                elif ' ' in names:
                    names = _comma_space_re.sub('\n', names)
                else:
                    # CSV without spaces
                    names = names.replace(',', '\n')

                names = _e_number_re.sub('', names)
                names = names.split('\n')
                names = (
                    name.strip() for name in names if _is_name_valid(name))
                return names
    return []


_invalid_name_re = re.compile(r'\[\d*\]')


def _is_name_valid(name):
    if name is None:
        return False
    name = name.strip()
    invalid_names = ['and', 'or']
    is_invalid = name.strip() in invalid_names or _invalid_name_re.search(name) is not None
    contains_e_number = _contains_the_word_e_number(name)
    is_e_number = _e_number_re.search(name) is not None

    length = len(name)
    is_valid_length = 1 < length < 25
    return not is_invalid and not is_e_number and not contains_e_number and not name.isspace() and is_valid_length


def _get_e_number_variations(e_number):
    e_number_with_space = e_number.replace('E', 'E ')
    return [e_number, e_number.lower(), e_number_with_space, e_number_with_space.lower()]


def _create_item_entry(name, e_number, sources, alternative_names):
    INDENTATION = '    '
    item = f'''
[[items]]
name = "{name}"
alternative_names = ['''

    alternative_names = list(alternative_names)
    if len(alternative_names) > 0:
        alternative_names = (
            f'{INDENTATION}"{name}"' for name in alternative_names)
        names = ',\n'.join(alternative_names)
        item += '\n'
        item += names
        item += '\n'

    item += f''']
e_number = "{e_number}"
state = "vegan"
description = ""
sources = [
'''
    for source in sources:
        item += f'{INDENTATION}{{ type = "url", value = "{source}" }},\n'

    item += f'''{INDENTATION}{{ type = "url", value = "https://elated.co.za/which-e-numbers-are-vegan/" }}
]
vegan_alternatives = []
'''
    return item


_FILENAME = 'imported_vegan.toml'


def _get_items(e_numbers):
    items = []
    for e_number in e_numbers:
        wikipedia_soup = _get_soup(_E_NUMBERS_URL)
        e_number_soup, title_soup = _get_wikipedia_e_number_and_title_table_data(
            wikipedia_soup, e_number)
        wikipedia_url = _get_wikipedia_url(e_number_soup, title_soup)
        name = _get_e_number_title(title_soup)

        sources = [wikipedia_url]

        uk_food_guide_url = _get_uk_food_guide_url(e_number)
        if uk_food_guide_url is not None:
            sources.append(uk_food_guide_url)

        article_soup = _get_soup(wikipedia_url)
        alternative_names = _get_alternative_names(article_soup, e_number)

        item = _create_item_entry(name, e_number, sources, alternative_names)
        items.append(item)
        print(f'Created item {e_number}')
    return items


def _chunks(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())


if __name__ == "__main__":
    worker_count = multiprocessing.cpu_count() - 1
    items = None
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        item_count = len(VEGAN_E_NUMBERS)
        items_per_worker = int(item_count / worker_count)
        print(f'item count: {item_count}')
        print(f'worker count: {worker_count}')
        print(f'items per worker: {items_per_worker}')

        futures = []

        if worker_count > 0:
            all_worker_items = VEGAN_E_NUMBERS[items_per_worker:]
            chunks = _chunks(all_worker_items, items_per_worker)
            for index, worker_items in enumerate(chunks):
                print(f'Running worker #{index} with items {worker_items}')
                future = executor.submit(_get_items, worker_items)
                futures.append(future)

        main_thread_items = VEGAN_E_NUMBERS[:items_per_worker]
        print(f'Running main thread with items {main_thread_items}')
        items = _get_items(main_thread_items)

        for future in futures:
            items.append(future.result())

    with open(_FILENAME, 'w') as the_file:
        for item in items:
            the_file.write(item)
