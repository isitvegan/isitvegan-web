#!/usr/bin/env python3

from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.request
import requests
import re
import os
from itertools import islice, chain
from concurrent.futures import ThreadPoolExecutor, Future
import multiprocessing
from pprint import pprint

E_NUMBERS = [
    # The following were already added manually
    # ("E100", "vegan"),
    # ("E101", "vegan"),
    # ("E101a", "vegan"),
    # ("E102", "vegan"),
    # ("E103", "vegan"),
    # ("E104", "vegan"),
    # ("E105", "vegan"),
    # ("E106", "vegan"),
    # ("E107", "vegan"),
    # ("E110", "vegan"),
    # ("E111", "vegan"),
    # ("E121", "vegan"),
    # ("E122", "vegan"),
    # ("E123", "vegan"),
    # ("E124", "vegan"),
    # ("E125", "vegan"),
    # ("E126", "vegan"),
    # ("E127", "vegan"),
    # ("E128", "vegan"),
    # ("E129", "vegan"),
    # ("E130", "vegan"),
    # ("E131", "vegan"),
    # ("E132", "vegan"),
    ("E133", "vegan"),
    ("E140", "vegan"),
    ("E141", "vegan"),
    ("E142", "vegan"),
    ("E143", "vegan"),
    ("E150a", "vegan"),
    ("E150b", "vegan"),
    ("E150c", "vegan"),
    ("E150d", "vegan"),
    ("E151", "vegan"),
    ("E152", "vegan"),
    ("E154", "vegan"),
    ("E155", "vegan"),
    ("E160a", "vegan"),
    ("E160b", "vegan"),
    ("E160c", "vegan"),
    ("E160d", "vegan"),
    ("E160e", "vegan"),
    ("E160f", "vegan"),
    ("E161a", "vegan"),
    ("E161b", "vegan"),
    ("E161c", "vegan"),
    ("E161d", "vegan"),
    ("E161e", "vegan"),
    ("E161f", "vegan"),
    ("E162", "vegan"),
    ("E163", "vegan"),
    ("E170", "vegan"),
    ("E171", "vegan"),
    ("E172", "vegan"),
    ("E173", "vegan"),
    ("E174", "vegan"),
    ("E175", "vegan"),
    ("E180", "vegan"),
    ("E181", "vegan"),

    ("E200", "vegan"),
    ("E201", "vegan"),
    ("E202", "vegan"),
    ("E203", "vegan"),
    ("E210", "vegan"),
    ("E211", "vegan"),
    ("E212", "vegan"),
    ("E213", "vegan"),
    ("E214", "vegan"),
    ("E215", "vegan"),
    ("E216", "vegan"),
    ("E217", "vegan"),
    ("E218", "vegan"),
    ("E219", "vegan"),
    ("E220", "vegan"),
    ("E221", "vegan"),
    ("E222", "vegan"),
    ("E223", "vegan"),
    ("E224", "vegan"),
    ("E225", "vegan"),
    ("E226", "vegan"),
    ("E227", "vegan"),
    ("E228", "vegan"),
    ("E230", "vegan"),
    ("E231", "vegan"),
    ("E232", "vegan"),
    ("E233", "vegan"),
    ("E234", "vegan"),
    ("E235", "vegan"),
    ("E236", "vegan"),
    ("E237", "vegan"),
    ("E238", "vegan"),
    ("E239", "vegan"),
    ("E240", "vegan"),
    ("E242", "vegan"),
    ("E249", "vegan"),
    ("E250", "vegan"),
    ("E251", "vegan"),
    ("E260", "vegan"),
    ("E261", "vegan"),
    ("E262", "vegan"),
    ("E263", "vegan"),
    ("E264", "vegan"),
    ("E280", "vegan"),
    ("E281", "vegan"),
    ("E282", "vegan"),
    ("E283", "vegan"),
    ("E284", "vegan"),
    ("E285", "vegan"),
    ("E290", "vegan"),
    ("E296", "vegan"),
    ("E297", "vegan"),

    ("E300", "vegan"),
    ("E301", "vegan"),
    ("E302", "vegan"),
    ("E303", "vegan"),
    ("E304", "vegan"),
    ("E306", "vegan"),
    ("E307", "vegan"),
    ("E308", "vegan"),
    ("E309", "vegan"),
    ("E310", "vegan"),
    ("E311", "vegan"),
    ("E312", "vegan"),
    ("E315", "vegan"),
    ("E316", "vegan"),
    ("E317", "vegan"),
    ("E318", "vegan"),
    ("E319", "vegan"),
    ("E320", "vegan"),
    ("E321", "vegan"),
    ("E329", "vegan"),
    ("E330", "vegan"),
    ("E331", "vegan"),
    ("E332", "vegan"),
    ("E333", "vegan"),
    ("E334", "vegan"),
    ("E335", "vegan"),
    ("E336", "vegan"),
    ("E337", "vegan"),
    ("E338", "vegan"),
    ("E339", "vegan"),
    ("E340", "vegan"),
    ("E341", "vegan"),
    ("E343", "vegan"),
    ("E350", "vegan"),
    ("E351", "vegan"),
    ("E352", "vegan"),
    ("E353", "vegan"),
    ("E354", "vegan"),
    ("E355", "vegan"),
    ("E356", "vegan"),
    ("E357", "vegan"),
    ("E363", "vegan"),
    ("E365", "vegan"),
    ("E366", "vegan"),
    ("E367", "vegan"),
    ("E370", "vegan"),
    ("E375", "vegan"),
    ("E380", "vegan"),
    ("E381", "vegan"),
    ("E385", "vegan"),
    ("E400", "vegan"),
    ("E401", "vegan"),
    ("E402", "vegan"),
    ("E403", "vegan"),
    ("E404", "vegan"),
    ("E405", "vegan"),
    ("E406", "vegan"),
    ("E407", "vegan"),
    ("E407a", "vegan"),
    ("E410", "vegan"),
    ("E412", "vegan"),
    ("E413", "vegan"),
    ("E414", "vegan"),
    ("E415", "vegan"),
    ("E416", "vegan"),
    ("E417", "vegan"),
    ("E418", "vegan"),
    ("E420", "vegan"),
    ("E421", "vegan"),
    ("E425", "vegan"),
    ("E440", "vegan"),
    ("E444", "vegan"),
    ("E445", "vegan"),
    ("E450", "vegan"),
    ("E451", "vegan"),
    ("E452", "vegan"),
    ("E459", "vegan"),
    ("E460", "vegan"),
    ("E461", "vegan"),
    ("E462", "vegan"),
    ("E463", "vegan"),
    ("E464", "vegan"),
    ("E465", "vegan"),
    ("E466", "vegan"),
    ("E468", "vegan"),
    ("E469", "vegan"),

    ("E500", "vegan"),
    ("E501", "vegan"),
    ("E503", "vegan"),
    ("E504", "vegan"),
    ("E507", "vegan"),
    ("E508", "vegan"),
    ("E509", "vegan"),
    ("E510", "vegan"),
    ("E511", "vegan"),
    ("E512", "vegan"),
    ("E513", "vegan"),
    ("E517", "vegan"),
    ("E518", "vegan"),
    ("E519", "vegan"),
    ("E520", "vegan"),
    ("E521", "vegan"),
    ("E522", "vegan"),
    ("E523", "vegan"),
    ("E524", "vegan"),
    ("E525", "vegan"),
    ("E526", "vegan"),
    ("E527", "vegan"),
    ("E528", "vegan"),
    ("E529", "vegan"),
    ("E530", "vegan"),
    ("E535", "vegan"),
    ("E536", "vegan"),
    ("E538", "vegan"),
    ("E540", "vegan"),
    ("E541", "vegan"),
    ("E543", "vegan"),
    ("E544", "vegan"),
    ("E545", "vegan"),
    ("E550", "vegan"),
    ("E551", "vegan"),
    ("E552", "vegan"),
    ("E553b", "vegan"),
    ("E554", "vegan"),
    ("E555", "vegan"),
    ("E556", "vegan"),
    ("E558", "vegan"),
    ("E559", "vegan"),
    ("E574", "vegan"),
    ("E575", "vegan"),
    ("E576", "vegan"),
    ("E577", "vegan"),
    ("E578", "vegan"),
    ("E579", "vegan"),

    ("E620", "vegan"),
    ("E621", "vegan"),
    ("E622", "vegan"),
    ("E623", "vegan"),
    ("E624", "vegan"),
    ("E625", "vegan"),
    ("E626", "vegan"),
    ("E628", "vegan"),
    ("E629", "vegan"),
    ("E630", "vegan"),
    ("E632", "vegan"),
    ("E633", "vegan"),
    ("E634", "vegan"),
    ("E636", "vegan"),
    ("E637", "vegan"),

    ("E900", "vegan"),
    ("E902", "vegan"),
    ("E903", "vegan"),
    ("E905", "vegan"),
    ("E905a", "vegan"),
    ("E905b", "vegan"),
    ("E905c", "vegan"),
    ("E906", "vegan"),
    ("E907", "vegan"),
    ("E908", "vegan"),
    ("E912", "vegan"),
    ("E914", "vegan"),
    ("E915", "vegan"),
    ("E922", "vegan"),
    ("E923", "vegan"),
    ("E924", "vegan"),
    ("E925", "vegan"),
    ("E926", "vegan"),
    # Seems to be a typo, should probably be E927a
    # ("E927", "vegan"),
    ("E927a", "vegan"),
    # Seems to be a typo, should probably be E927b
    # ("E297b", "vegan"),
    ("E927b", "vegan"),
    ("E928", "vegan"),
    ("E930", "vegan"),
    ("E938", "vegan"),
    ("E939", "vegan"),
    ("E940", "vegan"),
    ("E941", "vegan"),
    ("E942", "vegan"),
    ("E943a", "vegan"),
    ("E943b", "vegan"),
    ("E944", "vegan"),
    ("E948", "vegan"),
    ("E949", "vegan"),
    ("E950", "vegan"),
    ("E951", "vegan"),
    ("E952", "vegan"),
    ("E953", "vegan"),
    ("E954", "vegan"),
    ("E955", "vegan"),
    ("E957", "vegan"),
    ("E959", "vegan"),
    ("E965", "vegan"),
    ("E967", "vegan"),
    ("E999", "vegan"),

    ("E1103", "vegan"),
    # The following don't seem to exist
    # ("E1106", "vegan"),
    # ("E1107", "vegan"),
    # ("E1108", "vegan"),
    # ("E1109", "vegan"),
    # ("E1110", "vegan"),
    # ("E1111", "vegan"),
    # ("E1112", "vegan"),
    # ("E1113", "vegan"),
    # ("E1114", "vegan"),
    # ("E1115", "vegan"),
    # ("E1116", "vegan"),
    # ("E1117", "vegan"),
    # ("E1118", "vegan"),
    # ("E1119", "vegan"),
    # ("E1120", "vegan"),
    # ("E1121", "vegan"),
    # ("E1122", "vegan"),
    # ("E1123", "vegan"),
    # ("E1124", "vegan"),
    # ("E1125", "vegan"),
    # ("E1126", "vegan"),
    # ("E1127", "vegan"),
    # ("E1128", "vegan"),
    # ("E1129", "vegan"),
    # ("E1130", "vegan"),
    # ("E1131", "vegan"),
    # ("E1132", "vegan"),
    # ("E1133", "vegan"),
    # ("E1134", "vegan"),
    # ("E1135", "vegan"),
    # ("E1136", "vegan"),
    # ("E1137", "vegan"),
    # ("E1138", "vegan"),
    # ("E1139", "vegan"),
    # ("E1140", "vegan"),
    # ("E1141", "vegan"),
    # ("E1142", "vegan"),
    # ("E1143", "vegan"),
    # ("E1144", "vegan"),
    # ("E1145", "vegan"),
    # ("E1146", "vegan"),
    # ("E1147", "vegan"),
    # ("E1148", "vegan"),
    # ("E1149", "vegan"),
    # ("E1150", "vegan"),
    # ("E1151", "vegan"),
    # ("E1152", "vegan"),
    # ("E1153", "vegan"),
    # ("E1154", "vegan"),
    # ("E1155", "vegan"),
    # ("E1156", "vegan"),
    # ("E1157", "vegan"),
    # ("E1158", "vegan"),
    # ("E1159", "vegan"),
    # ("E1160", "vegan"),
    # ("E1161", "vegan"),
    # ("E1162", "vegan"),
    # ("E1163", "vegan"),
    # ("E1164", "vegan"),
    # ("E1165", "vegan"),
    # ("E1166", "vegan"),
    # ("E1167", "vegan"),
    # ("E1168", "vegan"),
    # ("E1169", "vegan"),
    # ("E1170", "vegan"),
    # ("E1171", "vegan"),
    # ("E1172", "vegan"),
    # ("E1173", "vegan"),
    # ("E1174", "vegan"),
    # ("E1175", "vegan"),
    # ("E1176", "vegan"),
    # ("E1177", "vegan"),
    # ("E1178", "vegan"),
    # ("E1179", "vegan"),
    # ("E1180", "vegan"),
    # ("E1181", "vegan"),
    # ("E1182", "vegan"),
    # ("E1183", "vegan"),
    # ("E1184", "vegan"),
    # ("E1185", "vegan"),
    # ("E1186", "vegan"),
    # ("E1187", "vegan"),
    # ("E1188", "vegan"),
    # ("E1189", "vegan"),
    # ("E1190", "vegan"),
    # ("E1191", "vegan"),
    # ("E1192", "vegan"),
    # ("E1193", "vegan"),
    # ("E1194", "vegan"),
    # ("E1195", "vegan"),
    # ("E1196", "vegan"),
    # ("E1197", "vegan"),
    # ("E1198", "vegan"),
    # ("E1199", "vegan"),
    ("E1200", "vegan"),
    ("E1201", "vegan"),
    ("E1202", "vegan"),
    ("E1400", "vegan"),
    ("E1401", "vegan"),
    ("E1402", "vegan"),
    ("E1403", "vegan"),
    ("E1404", "vegan"),
    ("E1410", "vegan"),
    ("E1412", "vegan"),
    ("E1413", "vegan"),
    ("E1414", "vegan"),
    ("E1420", "vegan"),
    ("E1421", "vegan"),
    ("E1422", "vegan"),
    ("E1430", "vegan"),
    ("E1440", "vegan"),
    ("E1441", "vegan"),
    ("E1442", "vegan"),
    ("E1450", "vegan"),
    ("E1451", "vegan"),
    ("E1505", "vegan"),
    ("E1510", "vegan"),
    ("E1518", "vegan"),
    ("E1520", "vegan"),

    # Already added manually
    # ("E120", "carnist"),
    ("E441", "carnist"),
    ("E542", "carnist"),
    ("E901", "carnist"),
    ("E904", "carnist"),
    ("E910", "carnist"),
    ("E913", "carnist"),
    ("E966", "carnist"),

    ("E153", "itDepends"),
    ("E161g", "itDepends"),
    ("E161h", "itDepends"),
    ("E161i", "itDepends"),
    ("E161j", "itDepends"),
    ("E252", "itDepends"),
    ("E270", "itDepends"),
    ("E322", "itDepends"),
    ("E325", "itDepends"),
    ("E326", "itDepends"),
    ("E327", "itDepends"),
    ("E422", "itDepends"),
    ("E430", "itDepends"),
    ("E431", "itDepends"),
    ("E432", "itDepends"),
    ("E433", "itDepends"),
    ("E434", "itDepends"),
    ("E435", "itDepends"),
    ("E436", "itDepends"),
    ("E442", "itDepends"),
    ("E470a", "itDepends"),
    ("E470b", "itDepends"),
    ("E471", "itDepends"),
    ("E472a", "itDepends"),
    ("E472b", "itDepends"),
    ("E472c", "itDepends"),
    ("E472d", "itDepends"),
    ("E472e", "itDepends"),
    ("E472f", "itDepends"),
    ("E473", "itDepends"),
    ("E474", "itDepends"),
    ("E475", "itDepends"),
    ("E476", "itDepends"),
    ("E477", "itDepends"),
    ("E478", "itDepends"),
    ("E479b", "itDepends"),
    ("E481", "itDepends"),
    ("E482", "itDepends"),
    ("E483", "itDepends"),
    ("E491", "itDepends"),
    ("E492", "itDepends"),
    ("E493", "itDepends"),
    ("E494", "itDepends"),
    ("E495", "itDepends"),
    ("E570", "itDepends"),
    ("E572", "itDepends"),
    ("E585", "itDepends"),
    ("E627", "itDepends"),
    ("E631", "itDepends"),
    ("E635", "itDepends"),
    ("E640", "itDepends"),
    ("e920", "itDepends"),
    ("E921", "itDepends"),
    ("E1105", "itDepends"),
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


_italic_re = re.compile(r'</?i>')
_a_re = re.compile(r'</?a( href=".*")?( title=".*")?>')

_non_dot_re = re.compile(r'\n([^•])')
_dot_re = re.compile(r'\s*•')

_non_semicolon_re = re.compile(r'\n([^;])')
_semicolon_re = re.compile(r'\s*;')

_comma_space_re = re.compile(r'\s*, ')

_e_number_re = re.compile(r'\b[Ee] *\d+\w*')


def _get_alternative_names(article_soup, e_number):
    info_box = article_soup.find(class_=re.compile(r'\s*infobox\s+.*'))
    if info_box is None:
        return []
    for style in info_box.find_all('style'):
        style.decompose() # decompose = "remove this tag and all its children"
    for row in info_box.find_all('tr'):
        for data in row.find_all('td'):
            text = data.get_text()
            ALTERNATIVE_NAMES_IDENTIFIER = "Other names"
            if ALTERNATIVE_NAMES_IDENTIFIER in text:
                list = data.find('ul')
                if list is not None:
                    # Some cleaned up articles correctly use a
                    # list instead of some garbled junk.
                    items = list.find_all('li')
                    names = (_extract_name(item) for item in items)
                    return (name for name in names if _is_name_valid_2(name))
                else:
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

_citation_re = re.compile(r'\[\d*\]')
def _extract_name(item) -> str:
    name = item.get_text()
    name = _citation_re.sub('', name)
    return (name
        .strip()
        .rstrip(';')
        .replace('[citation needed]', ''))

# Is name valid for nice lists, so less heuristics necessary
def _is_name_valid_2(name: str) -> bool:
    return (name is not None
        and name != ''
        and not _contains_the_word_e_number(name)
        and _e_number_re.search(name) is None)

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


def _create_item_entry(name, e_number, sources, alternative_names, state):
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
state = "{state}"
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


_FILENAME = 'e_numbers.toml'


def _get_items(e_numbers):
    items = []
    for e_number, state in e_numbers:
        wikipedia_soup = _get_soup(_E_NUMBERS_URL)
        e_number_soup, title_soup = _get_wikipedia_e_number_and_title_table_data(
            wikipedia_soup, e_number)
        wikipedia_url = _get_wikipedia_url(e_number_soup, title_soup)
        name = _get_e_number_title(title_soup)

        sources = [wikipedia_url]

        article_soup = _get_soup(wikipedia_url)
        alternative_names = [n for n in _get_alternative_names(article_soup, e_number) if n != name]

        item = _create_item_entry(
            name, e_number, sources, alternative_names, state)
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
        item_count = len(E_NUMBERS)
        items_per_worker = int(item_count / worker_count)
        print(f'item count: {item_count}')
        print(f'worker count: {worker_count}')
        print(f'items per worker: {items_per_worker}')

        futures = []

        if worker_count > 0:
            all_worker_items = E_NUMBERS[items_per_worker:]
            chunks = _chunks(all_worker_items, items_per_worker)
            for index, worker_items in enumerate(chunks):
                print(f'Running worker #{index} with the following items.')
                pprint(worker_items)
                future = executor.submit(_get_items, worker_items)
                futures.append(future)

        main_thread_items = E_NUMBERS[:items_per_worker]
        print(f'Running main thread with the following items.')
        pprint(main_thread_items)
        items = _get_items(main_thread_items)

        for future in futures:
            items.append(future.result())

    items = chain(*items)
    print(f'Finished creating items, writing them to {_FILENAME}')
    with open(_FILENAME, 'w') as import_file:
        for item in items:
            import_file.write(item)

    print('All done!')
