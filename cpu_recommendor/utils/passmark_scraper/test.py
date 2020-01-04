import constants
from scraper import scrape_page
from data_merger import merge_data
import json
from os.path import join

with open(join(constants.base_directory, 'passmark_scraper', 'scraped_data', constants.passmark_filename), 'r') as fp:
    scraped_data = json.load(fp)

complete_data = merge_data(scraped_data)
test_data = complete_data['AMD Ryzen 7 3700X']
clock = test_data['base_clock']

test = scrape_page(constants.high_end_cpus)