#!/usr/bin/env python3

from bs4 import BeautifulSoup, NavigableString, Tag
import urllib.request
import requests
import re

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
    "E1106",
    "E1107",
    "E1108",
    "E1109",
    "E1110",
    "E1111",
    "E1112",
    "E1113",
    "E1114",
    "E1115",
    "E1116",
    "E1117",
    "E1118",
    "E1119",
    "E1120",
    "E1121",
    "E1122",
    "E1123",
    "E1124",
    "E1125",
    "E1126",
    "E1127",
    "E1128",
    "E1129",
    "E1130",
    "E1131",
    "E1132",
    "E1133",
    "E1134",
    "E1135",
    "E1136",
    "E1137",
    "E1138",
    "E1139",
    "E1140",
    "E1141",
    "E1142",
    "E1143",
    "E1144",
    "E1145",
    "E1146",
    "E1147",
    "E1148",
    "E1149",
    "E1150",
    "E1151",
    "E1152",
    "E1153",
    "E1154",
    "E1155",
    "E1156",
    "E1157",
    "E1158",
    "E1159",
    "E1160",
    "E1161",
    "E1162",
    "E1163",
    "E1164",
    "E1165",
    "E1166",
    "E1167",
    "E1168",
    "E1169",
    "E1170",
    "E1171",
    "E1172",
    "E1173",
    "E1174",
    "E1175",
    "E1176",
    "E1177",
    "E1178",
    "E1179",
    "E1180",
    "E1181",
    "E1182",
    "E1183",
    "E1184",
    "E1185",
    "E1186",
    "E1187",
    "E1188",
    "E1189",
    "E1190",
    "E1191",
    "E1192",
    "E1193",
    "E1194",
    "E1195",
    "E1196",
    "E1197",
    "E1198",
    "E1199",
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


def _get_first_table_data(haystack, needle):
    for index, item in enumerate(haystack):
        item_text = item.get_text().strip()
        if item_text == needle:
            return index
    return None


def _get_wikipedia_url(item):
    sanitized_item = item.replace('/wiki/', '')
    return f'https://en.wikipedia.org/wiki/{sanitized_item}'


def _get_soup(url):
    content = urllib.request.urlopen(url)
    return BeautifulSoup(content, 'html.parser')


def _get_wikipedia_title(wikipedia_soup):
    return wikipedia_soup.find(id='firstHeading').get_text().strip()


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


def _resolve_disambiguation(wikipedia_soup):
    disambiguation_title = _get_wikipedia_title(wikipedia_soup)
    possible_pages = wikipedia_soup.find(
        id='mw-content-text').find('ul').find_all('li')
    for possible_page in possible_pages:
        possible_page_text = possible_page.get_text().strip()
        if _contains_the_word_e_number(possible_page_text) or 'additive' in possible_page_text:
            for link in possible_page.find_all('a', href=True):
                wikipedia_url = _get_wikipedia_url(link['href'])
                wikipedia_soup = _get_soup(wikipedia_url)
                name = _get_wikipedia_title(wikipedia_soup)
                if not _contains_the_word_e_number(name):
                    return wikipedia_url, wikipedia_soup, name

    # Fallback: Just take the first one
    for link in possible_pages[0].find_all('a', href=True):
        wikipedia_url = _get_wikipedia_url(link['href'])
        wikipedia_soup = _get_soup(wikipedia_url)
        name = _get_wikipedia_title(wikipedia_soup)
        if not _contains_the_word_e_number(name):
            return wikipedia_url, wikipedia_soup, name

    raise ValueError(
        f'Disambiguation could not be resolved for page {disambiguation_title}')


def _get_uk_food_guide_url(e_number):
    e_number = e_number.lower()
    url = f'http://www.ukfoodguide.net/{e_number}.htm'
    status_code = requests.head(url).status_code
    if status_code is 200:
        return url
    else:
        return None


def _get_alternative_names(wikipedia_soup, e_number):
    info_box = wikipedia_soup.find(class_='infobox bordered')
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
                html = re.sub(r'</?i>', '', html)
                html = re.sub(r'</?a( href=".*")?( title=".*")?>', '', html)

                data = BeautifulSoup(html, 'html.parser')

                name_list = data.get_text("\n")
                names = name_list.replace(ALTERNATIVE_NAMES_IDENTIFIER, '')
                names = names.strip()
                names = names.replace('\n ', ' ')
                names = names.strip()
                if '•' in names:
                    names = re.sub(r'\n([^•])', r'$1', names)
                    names = re.sub(r'\s*•', '\n', names)
                elif ';' in names:
                    names = re.sub(r'\n([^;])', r'\1', names)
                    names = re.sub(r'\s*;', '\n', names)
                elif ' ' in names:
                    names = re.sub(r'\s*, ', '\n', names)
                else:
                    # CSV without spaces
                    names = re.sub(r',', '\n', names)

                names = re.sub(r'[^\w][Ee] *\d+\w*', '', names)
                names = names.split('\n')
                names = (
                    name.strip() for name in names if _is_name_valid(name))
                return names
    return []


def _is_name_valid(name):
    if name is None:
        return False
    name = name.strip()
    invalid_names = ['and', 'or']
    is_invalid = name.strip() in invalid_names
    is_e_number = _contains_the_word_e_number(name)

    length = len(name)
    is_valid_length = 1 < length < 25
    return not is_invalid and not is_e_number and not name.isspace() and is_valid_length


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
description = """
"""
sources = [
'''
    for source in sources:
        item += f'{INDENTATION}{{ type = "url", value = "{source}" }},\n'

    item += f'''{INDENTATION}{{ type = "url", value = "https://elated.co.za/which-e-numbers-are-vegan/" }}
]
vegan_alternatives = []
'''
    return item


for e_number in VEGAN_E_NUMBERS:
    wikipedia_url = _get_wikipedia_url(e_number)
    wikipedia_soup = _get_soup(wikipedia_url)
    name = _get_wikipedia_title(wikipedia_soup)

    if name == e_number:
        wikipedia_url, wikipedia_soup, name = _resolve_disambiguation(
            wikipedia_soup)

    sources = [wikipedia_url]
    uk_food_guide_url = _get_uk_food_guide_url(e_number)
    if uk_food_guide_url is not None:
        sources.append(uk_food_guide_url)

    alternative_names = _get_alternative_names(wikipedia_soup, e_number)

    item = _create_item_entry(name, e_number, sources, alternative_names)
    print(item)
