import requests
import logging
from bs4 import BeautifulSoup
from configobj import ConfigObj
from multiprocessing import Pool, Manager, cpu_count
from time import sleep
from os.path import join 
from .cpu_scraper import get_cpu_info
from .gpu_scraper import get_gpu_info
from . import constants

logger = logging.getLogger(__name__)

class PassmarkScraper():
    def __init__(self, part):
        self.part = part
        self.urls = constants.part_urls[part]
        self._function = f'get_{part}_info'
        
    def scrape_page(self, url, parser='html.parser'):
        manager = Manager() #Manager manages shared memory objects
        pool = Pool(cpu_count())
        data_dict = manager.dict() #Our dictionary can now be shared between threads

        page = requests.get(url)
        soup = BeautifulSoup(page.content, parser)
        
        list_container = soup.find(class_='chartlist')
        parts = list_container.find_all('li')
        part_info = [part.find(class_='name') for part in parts]
        part_urls = [part.get('href') for part in part_info]

        for url in part_urls: #Each task is added to the pool to be completed in parallel
            pool.apply_async(eval(self._function), args=(url, data_dict, parser))

        pool.close()
        cnt = 0
        while pool._cache and cnt <= constants.timeout_threshold: #We wait until all the processes are finished
            sleep(constants.time_increment)
            cnt += constants.time_increment
        
        if cnt >= constants.timeout_threshold:
            logging.warning('Scraper timed out!!')
        logging.info('Scraping Complete!')
        logging.info(f'Traversing {len(part_urls)} pages and capturing {len(data_dict)} entries took {cnt} seconds!')

        return data_dict

    def get_data(self):
        final_dict = {}
        
        for url in self.urls:
            data_dict = self.scrape_page(url)
            final_dict = {**final_dict, **data_dict}
        
        return final_dict
            