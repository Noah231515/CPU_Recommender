import logging
import json
from . import constants
from os.path import join
from sys import exit
from pcpartpicker import API

logging.basicConfig(filename=join(constants.passmark_log_directory, 'data_merger', 'data_merger.log'), level=logging.DEBUG)



def fix_clock_speeds(cpu):
    to_ghz = 1000000000
    cpu.__dict__['base_clock'] = cpu.base_clock.cycles/to_ghz
    
    if cpu.boost_clock:
        cpu.__dict__['boost_clock'] = cpu.boost_clock.cycles/to_ghz
    
def fix_scraped_price(scraped_cpu): #Removes dollar sign, and commas
    scraped_price = scraped_cpu['price'][1:]
    scraped_price = scraped_price.replace(',', '')
    return float(scraped_price)

def merge_data(scraped_data, dump_data=False):
    logging.info('Merging Start')
    merged_data = {}    
    api = API()
    api_cpu_data = api.retrieve('cpu', force_refresh=True)['cpu']

    for i, cpu in enumerate(api_cpu_data):
        cpu_name = ' '.join([cpu.brand, cpu.model])

        if 'Threadripper' in cpu_name:
            cpu_name = ' '.join([cpu.brand, 'Ryzen', cpu.model])
            
        try: #May not work, because we're merging data from pcpartpicker to data found on pcmark
            scraped_cpu = scraped_data[cpu_name]
            scraped_price = fix_scraped_price(scraped_cpu)
            partpick_price = float(cpu.price.amount)
            
            if not scraped_price or not cpu.price.amount:
                price = max([scraped_price, partpick_price])
            else:
                price = (scraped_price + partpick_price)/2
            
            fix_clock_speeds(cpu)
            merged_cpu_data = {**scraped_cpu, **cpu.__dict__, 'price': price}    
            merged_data[cpu_name] = merged_cpu_data
            logging.info(f'CPU Captured! CPU name: {cpu_name}, passmark_price: {scraped_price}, pcpartpicker_price: {cpu.price.amount}, final_price: {price}, index: {i}')
            

        except Exception:
            logging.debug(f'CPU Not Captured! Data: {cpu} ')
            pass

    if dump_data:
        with open(join(constants.base_directory, 'passmark_scraper', 'scraped_data', 'merged_data.json'), 'w') as fp:
            json.dump(merged_data, fp)

    return merged_data

