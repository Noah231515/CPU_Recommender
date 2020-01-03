import requests
import constants
import logging
import re
import json
import traceback
from bs4 import BeautifulSoup
from configobj import ConfigObj
from multiprocessing import Pool, Manager, cpu_count
from time import sleep
from os.path import join 

logging.basicConfig(filename=join(constants.passmark_log_directory, 'scraper', 'scraper.log'), level=logging.DEBUG)

class Passmark_Scraper():
    def __init__(self, url=None, parser='html.parser'):
        self.url = url
        self.manager = Manager() #Manages shared memory objects
        self.pool = Pool(cpu_count()) #Stores tasks to be ran

        self.data_dict = self.manager.dict() #Shared object between processes
        self.data_list = []
        self.parser = parser

    @staticmethod
    def strip_text(container, regex):
        STRIP_REGEX = re.compile(regex)
        text = STRIP_REGEX.search(container)

        return text

    def get_cpu_info(self, cpu_url):
        full_url = constants.passmark_base_url + cpu_url
        page = requests.get(full_url)
        soup = BeautifulSoup(page.content, self.parser)

        try:
            name = soup.find(class_='cpuname').get_text().split('@')[0].strip()

            left_desc = soup.find(class_='left-desc-cpu').get_text()
            right_desc = soup.find(class_='right-desc').get_text()
            desc_foot = soup.find(class_='desc-foot').get_text()
            
            cpu_class = strip_text(left_desc, '(Class:\s+)(\S+)').group(2)

            if cpu_class and cpu_class.strip() != 'Desktop':
                return
        
            else:    
                
                socket = strip_text(left_desc, '(Socket:\s+)(\S+)').group(2)
                multithread_score = strip_text(right_desc, '(Average CPU Mark)(\n \d+)').group(2).strip()
                singlethread_score = strip_text(right_desc, '(Single Thread Rating:\s+)(\d+)').group(2).strip()
                samples = strip_text(right_desc, '(Samples:\s+)(\d+)').group(2) #used for weighting
                release_date = strip_text(desc_foot, '(CPU First Seen on Charts:\s+)(Q\d+\s\d+)').group(2) 
                price = strip_text(desc_foot, '\$(\d+[,.])*(\d+)').group()

                print(f'My name is {name}')

                self.data_dict[name] = {
                    'socket': socket,
                    'multithread_score': multithread_score,
                    'singlethread_score': singlethread_score,
                    'samples': samples,
                    'release_date': release_date,
                    'price': price
                    }
                    
        except:
            print('errors galore')
            print(traceback.format_exc())
            logging.debug(f'The CPU: {name} has missing data and will be skipped!')
                
    def scrape_page(self):
        logging.debug('Scraper starting!')
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, self.parser)
        
        list_container = soup.find(class_='chartlist')
        cpus = list_container.find_all('li')
        cpu_info = [cpu.find(class_='name') for cpu in cpus]
        cpu_urls = [cpu.get('href') for cpu in cpu_info]
        
        for url in cpu_urls: #Each task is added to the pool to be completed in parallel
            self.pool.apply_async(self.get_cpu_info, args=(url))
            #print(f'self: {self.__dict__}')

        
        self.pool.close()
        time_cnt = 0
        while self.pool._cache and time_cnt <= constants.timeout_threshold: #We wait until all the processes are finished
            sleep(constants.time_increment)
            time_cnt += constants.time_increment
        
        logging.info('Scraping Complete!')
        logging.info(f'Traversing {len(cpu_urls)} pages and capturing {len(self.data_dict)} entries took {time_cnt} seconds!')

        self.data_list.append(self.data_dict)
        self.data_dict = {}

if __name__ == '__main__':
    print('hello?')
    scraper = Passmark_Scraper(constants.high_end_cpus)
    scraper.scrape_page()
    high_end = scraper.data_list[0]
    print(high_end)
    # import data_merger as merger

    # high_end_cpus = scrape_page(constants.high_end_cpus)
    # common_cpus = scrape_page(constants.common_cpus)

    # cpu_data = {**high_end_cpus, **common_cpus}
    # with open(join(constants.base_directory, 'Passmark_scraper', 'scraped_data', constants.passmark_filename), 'w') as fp: 
    #     json.dump(cpu_data, fp)

    # try:
    #     merger.merge_data(cpu_data)
    #     logging.info('Merge complete!')

    # except:
    #     logging.error('Merging failed')
