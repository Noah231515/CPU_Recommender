from requests import get
import logging
from bs4 import BeautifulSoup
from configobj import ConfigObj
from multiprocessing import Pool, Manager, cpu_count
from time import sleep
from os.path import join 
from . import constants
from . import scraper_utils

logging.basicConfig(filename=join(constants.passmark_log_directory, 'scraper', 'scraper.log'), level=logging.DEBUG)

def get_cpu_info(url, data_dict, parser):
    full_url = constants.passmark_base_url + url
    page = get(full_url)
    soup = BeautifulSoup(page.content, parser)
    try:
        name = soup.find(class_='cpuname').get_text().split('@')[0].strip()
        name_split = name.split()
        brand = name_split[0]
        model = ' '.join(name_split[1:])

        #HTML containers found on the passmark website
        left_desc, right_desc, desc_foot = scraper_utils.get_page_containers(soup)  
        cpu_class = scraper_utils.strip_text(left_desc, '(Class:\s+)(\S+)').group(2)

        if cpu_class and cpu_class.strip() != 'Desktop':
            return
        else:    
            socket = scraper_utils.strip_text(left_desc, '(Socket:\s*)(\S+)').group(2)
            base_clock = scraper_utils.strip_text(left_desc, '(Clockspeed:\s*)(\d+\.\d+)').group(2)
            try:
                boost_clock = scraper_utils.strip_text(left_desc, '(Turbo Speed:\s*)(\d+\.\d+)').group(2)
            except AttributeError:
                boost_clock = None
            
            cores_match = scraper_utils.strip_text(left_desc, '(No of Cores:\s*)(\d+)\s*(\(2 logical cores per physical\))?')
            core_count = cores_match.group(2)
            multithreading = True if cores_match.group(3) else False
            tdp = scraper_utils.strip_text(left_desc, '(Typical TDP:\s*)(\d+)').group(2)
            multithread_score = scraper_utils.strip_text(right_desc, '(Average CPU Mark)(\n \d+)').group(2).strip()
            singlethread_score = scraper_utils.strip_text(right_desc, '(Single Thread Rating:\s+)(\d+)').group(2).strip()
            samples = scraper_utils.strip_text(right_desc, '(Samples:\s*)(\d+)').group(2) #used for weighting
            release_date = scraper_utils.strip_text(desc_foot, '(CPU First Seen on Charts:\s*)(Q\d+\s\d+)').group(2) 
            price = scraper_utils.strip_text(desc_foot, '\$((\d+[,.])*(\d+))').group(1).replace(',', '')
            image_url = scraper_utils.get_part_img(name, parser)

            data_dict[name] = {
                'brand': brand,
                'model': model,
                'socket': socket,
                'base_clock': base_clock,
                'boost_clock': boost_clock,
                'cores': core_count,
                'multithreading': multithreading,
                'tdp': tdp,
                'multithreaded_score': multithread_score,
                'singlethreaded_score': singlethread_score,
                'samples': samples,
                'release_date': release_date,
                'price': price,
                'image_url': image_url
                }
                
            return data_dict
            
    except AttributeError:
        logging.debug(f'The CPU: {name} has missing data and will be skipped!')
            
