import requests
import logging
import re
import json
from bs4 import BeautifulSoup
from configobj import ConfigObj
from multiprocessing import Pool, Manager, cpu_count
from time import sleep
from os.path import join 
from . import constants

logging.basicConfig(filename=join(constants.passmark_log_directory, 'scraper', 'scraper.log'), level=logging.DEBUG)

def strip_text(container, regex):
    STRIP_REGEX = re.compile(regex)
    text = STRIP_REGEX.search(container)

    return text

def get_cpu_info(url, data_dict, parser):
    full_url = constants.passmark_base_url + url
    page = requests.get( full_url )
    soup = BeautifulSoup(page.content, parser)

    try:
        name = soup.find(class_='cpuname').get_text().split('@')[0].strip()
        
        #HTML containers found on the passmark website
        left_desc = soup.find(class_='left-desc-cpu').get_text()
        right_desc = soup.find(class_='right-desc').get_text()
        desc_foot = soup.find(class_='desc-foot').get_text()
        
        cpu_class = strip_text(left_desc, '(Class:\s+)(\S+)').group(2)

        if cpu_class and cpu_class.strip() != 'Desktop':
            return
    
        else:    
            #print(f'Class: {cpu_class}, name: {name}')
            socket = strip_text(left_desc, '(Socket:\s+)(\S+)').group(2)
            multithread_score = strip_text(right_desc, '(Average CPU Mark)(\n \d+)').group(2).strip()
            singlethread_score = strip_text(right_desc, '(Single Thread Rating:\s+)(\d+)').group(2).strip()
            samples = strip_text(right_desc, '(Samples:\s+)(\d+)').group(2) #used for weighting
            release_date = strip_text(desc_foot, '(CPU First Seen on Charts:\s+)(Q\d+\s\d+)').group(2) 
            price = strip_text(desc_foot, '\$(\d+[,.])*(\d+)').group()

            data_dict[name] = {
                'socket': socket,
                'multithreaded_score': multithread_score,
                'singlethreaded_score': singlethread_score,
                'samples': samples,
                'release_date': release_date,
                'price': price
                }
            
            return data_dict
    except:
        logging.debug(f'The CPU: {name} has missing data and will be skipped!')
            
def scrape_page(url, parser='html.parser'):
    manager = Manager() #Manager manages shared memory objects
    
    pool = Pool(cpu_count())
    data_dict = manager.dict() #Our dictionary can now be shared between processes

    page = requests.get( url )
    soup = BeautifulSoup(page.content, parser)
    
    list_container = soup.find(class_='chartlist')
    cpus = list_container.find_all('li')
    cpu_info = [cpu.find(class_='name') for cpu in cpus]
    cpu_urls = [cpu.get('href') for cpu in cpu_info]

    for url in cpu_urls: #Each task is added to the pool to be completed in parallel
        pool.apply_async(get_cpu_info, args=(url, data_dict, parser) )

    pool.close()
    cnt = 0
    while pool._cache and cnt <= constants.timeout_threshold: #We wait until all the processes are finished
        sleep(constants.time_increment)
        cnt += constants.time_increment
    
    logging.info('Scraping Complete!')
    logging.info(f'Traversing {len(cpu_urls)} pages and capturing {len(data_dict)} entries took {cnt} seconds!')

    return data_dict

