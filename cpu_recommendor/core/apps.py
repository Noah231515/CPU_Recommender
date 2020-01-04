from django.apps import AppConfig
import logging
from pandas import DataFrame
from numpy import average
from sklearn.preprocessing import MinMaxScaler, normalize

logger = logging.getLogger('app_setup')

def test(cpu): #Prolly can use a dataframe for this
    #TESTING FOR PRODUCTION
    



    if not cpu.boost_clock:
        cpu.boost_clock = 0
    data_list = [
        (cpu.multithreaded_score, 4),
        (cpu.singlethreaded_score, 3),
        (cpu.base_clock, 3),
        (cpu.cores, 5),
        (cpu.boost_clock, 3),
        (100, 5)
    ]
    r_score = 0
    for tup in data_list:
        r_score+= tup[0]*tup[1]
    
    r_score /= 23
    print(f'For  {cpu.name}: {r_score} ')
    return r_score

def build_dataframe(cpu,task):
    cpu_df = DataFrame()
    weight_dict = {
        'p': [4,3,3,5,3,5],
        'g': [3,5,4,3,5,3]
    }

    cpu_df['features'] = [
        cpu.multithreaded_score,
        cpu.singlethreaded_score,
        cpu.base_clock,
        cpu.cores,
        cpu.boost_clock,
        int(cpu.multithreading) * 100
    ]
    cpu_df['wt'] = weight_dict[task]

    scaled = normalize(cpu_df)

    scaled_df = DataFrame(scaled)
    scaled_df.columns = ['features', 'wt']   

    return scaled_df

def compute_R_score(cpu, task='p'):
    if task not in ['a','p','g','b']: #productivity, gaming, blend
        return #this is an error
    else:
        cpu_df = build_dataframe(cpu,task)
        r_score = average(cpu_df['features'], weights=cpu_df['wt'])

        print(f"CPU: {cpu.name}, R_score: {r_score}, Task: {task} ")

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from utils.passmark_scraper.scraper import scrape_page
        from utils.passmark_scraper import constants
        from utils.passmark_scraper.data_merger import merge_data
        from .models import CPU 

        number_of_cpus = len(CPU.objects.all())
        test_cpu = CPU.objects.get(name='AMD Ryzen 7 3700X')
        test_cpu_2 = CPU.objects.all()[162]

        compute_R_score(test_cpu)
        compute_R_score(test_cpu, task='g')
        
        compute_R_score(test_cpu_2)
        compute_R_score(test_cpu_2, task='g')
        #compute_R_score(test_cpu_2)

        if not number_of_cpus:
            logger.info('Empty database. Populating beginning...')
            high_end_cpus = scrape_page(constants.high_end_cpus)
            common_cpus = scrape_page(constants.common_cpus)

            scraped_data = {**high_end_cpus, **common_cpus}
            merged_data = merge_data(scraped_data)
            
            for name, data in merged_data.items():
                data['name'] = name
                cpu = CPU(**data)
                cpu.save()

        

        
        #data = scrape_page(constants.high_end_cpus)
        #merged_data = merge_data(data)
        