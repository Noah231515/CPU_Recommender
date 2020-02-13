from . import constants
from re import compile
from requests import get
from bs4 import BeautifulSoup

def get_part_name(soup):
    name = soup.find(class_='cpuname').get_text().split('@')[0].strip()
    return name

def get_page_containers(soup):
    left_desc = soup.find(class_='left-desc-cpu').get_text()
    right_desc = soup.find(class_='right-desc').get_text()
    desc_foot = soup.find(class_='desc-foot').get_text()
    return left_desc, right_desc, desc_foot

def get_part_img(name, parser): #Takes the first image from google images
    params = {'q':name}
    page = get(constants.google_images, params)
    soup = BeautifulSoup(page.content, parser)
    img_tables = soup.find_all('table')[4]
    return img_tables.find('a').find('img')['src']

def strip_text(container, regex=None, key=None, replacement=None): #Can define a regex or use a reusable one
    if key and replacement:
        regex=constants.regex_strings[key].replace('{REPLACE_ME}', replacement)
        
        
    STRIP_REGEX = compile(regex)
    text = STRIP_REGEX.search(container)
    return text