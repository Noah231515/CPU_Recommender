import requests
import logging
import traceback
from bs4 import BeautifulSoup
from configobj import ConfigObj
from multiprocessing import Pool, Manager, cpu_count
from time import sleep
from os.path import join 
from . import constants
from . import scraper_utils

def get_gpu_info(url, data_dict, parser):
    
    full_url = constants.passmark_base_url_gpu + url
    page = requests.get(full_url)
    soup = BeautifulSoup(page.content, parser)
    if page.status_code == 200:
            
        try:
            name = scraper_utils.get_part_name(soup)
            left_desc, right_desc, desc_foot = scraper_utils.get_page_containers(soup)
            #print(f'Left desc: {left_desc}')
            gpu_class = scraper_utils.strip_text(left_desc, key='class', replacement='Videocard Category')
            if gpu_class and gpu_class != 'Desktop':
                return
            else:
                tdp = scraper_utils.strip_text(container=left_desc, key='generic_value', replacement='Max TDP').group(2)
                price = scraper_utils.strip_text(desc_foot, constants.regex_strings['price']).group(1)
                score = scraper_utils.strip_text(right_desc, key='score', replacement='Average G3D Mark').group(2).strip('\n')
                clock = scraper_utils.strip_text(left_desc, key='generic_value', replacement='Core Clock\(s\)').group(2)
                memory_size = scraper_utils.strip_text(left_desc, key='generic_value', replacement='Max Memory Size').group(2)
                memory_clock = scraper_utils.strip_text(left_desc, key='generic_value', replacement='Memory Clock\(s\)').group(2)
                directx = scraper_utils.strip_text(left_desc, key='generic_value', replacement='DirectX').group(2)

                data_dict[name] = {
                    'tdp': tdp,
                    'price': price,
                    'score': score,
                    'clock_speed': clock,
                    'memory_size': memory_size,
                    'memory_clock': memory_clock,
                    'directx': directx
                }
                
                print(f' Data: {data_dict}')
            
                


        except AttributeError:
            logging.debug(f'The CPU: {name} has missing data and will be skipped!')
            logging.debug(traceback.print_exc())
            #traceback.print_exc()
    else:
        logging.ERROR(f'The request to {full_url} is invalid!!. Response code: {page.status_code}')
    
    