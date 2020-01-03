import logging
import json
import constants
from os.path import join
from sys import exit
from pcpartpicker import API

logging.basicConfig(filename=join(constants.passmark_log_directory, 'data_merger', 'data_merger.log'), level=logging.DEBUG)
logging.info('Start')

try:
    with open(join(constants.base_directory, 'Passmark_scraper', 'scraped_data', constants.passmark_filename) ,'r') as fp:
        scraped_data = json.load(fp)

except FileNotFoundError as e:
    logging.error('CPU Data not found. Run scraper.py to generate the cpu data.')
    exit(0)

def fix_scraped_price(scraped_cpu): #Removes dollar sign, and commas
    scraped_price = scraped_cpu['price'][1:]
    scraped_price = scraped_price.replace(',', '')
    return float(scraped_price)

def merge_data(scraped_data): 
    merged_data = {}    
    api = API()
    api_cpu_data = api.retrieve('cpu')['cpu']

    for i, cpu in enumerate(api_cpu_data):
        cpu_name = ' '.join([cpu.brand, cpu.model])

        if 'Threadripper' in cpu_name:
            cpu_name = ' '.join([cpu.brand, 'Ryzen', cpu.model])
            
        try:
            scraped_cpu = scraped_data[cpu_name]
            scraped_price = fix_scraped_price(scraped_cpu)
            partpick_price = float(cpu.price.amount)

            if not scraped_price or not cpu.price.amount:
                price = max([scraped_price, partpick_price])
            else:
                price = (scraped_price + partpick_price)/2
        
            merged_cpu_data = {**scraped_cpu, **cpu.__dict__, 'price': price}    
            merged_data[cpu_name] = merged_cpu_data
            logging.info(f'CPU Captured! CPU name: {cpu_name}, passmark_price: {scraped_price}, pcpartpicker_price: {cpu.price.amount}, final_price: {price}, index: {i}')
            

        except Exception:
            logging.debug(f'CPU Not Captured! Data: {cpu} ')
            pass

    return merged_data

if __name__ == '__main__':
    merged_data = merge_data(scraped_data)
    print(merged_data)
    print(len(merged_data))