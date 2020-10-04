from django.apps import AppConfig
import logging
from pandas import DataFrame
from numpy import average
from sklearn.preprocessing import MinMaxScaler, normalize, minmax_scale
from django.conf import settings


logger = logging.getLogger(__name__)

def build_dataframe(cpu,task):
    cpu_df = DataFrame()
    weight_dict = {
        'p': [3,1,1.5,2.5,.5,1.5],
        'g': [1,3,1.5,.5,2.5,1.5]
    }
    if not cpu.boost_clock:
        cpu.boost_clock = float(0)

    cpu_df['features'] = [ #Values are scales scaled approprietly, so that no one feature dominates
        float(cpu.multithreaded_score)/1000, 
        float(cpu.singlethreaded_score)/100,
        float(cpu.base_clock)*10,
        float(cpu.cores),
        float(cpu.boost_clock)*10,
        float(cpu.multithreading) * 10
    ]
    cpu_df['wt'] = weight_dict[task] 
    logger.debug(f'Normal DF for {cpu.name}: {cpu_df}')
    return cpu_df

def compute_R_score(cpu, task='p'):
    if task not in ['a','p','g','b']: #productivity, gaming, blend
        return #this is an error

    if task == 'b' or task == 'a':
        prod = compute_R_score(cpu, 'p')
        gaming = compute_R_score(cpu, 'g')
        blend = (prod + gaming)/2

        if task == 'b':
            return blend
        else:
            return {'p': prod, 'g': gaming, 'b': blend}

    else:
        cpu_df = build_dataframe(cpu,task)
        r_score = average(cpu_df['features'], weights=cpu_df['wt'])
        logger.debug(f"CPU: {cpu.name}, R_score: {r_score}, Task: {task}")

        return r_score

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from utils.passmark_scraper.scraper import PassmarkScraper
        from .models import GPU, CPU

        print(settings.RUN_ARGS)
        if 'runserver' in settings.RUN_ARGS:
            #TODO: Debug cpu scraper. Not able to add any cpus to the db
            #number_of_cpus = len(CPU.objects.all())
            number_of_cpus = len(CPU.objects.all())
            number_of_gpus = len(GPU.objects.all())
            if not number_of_cpus:
                logger.info('No gpus in the database. Populating beginning...')
                scraper = PassmarkScraper("cpu")
                scraped_data = scraper.get_data()
                
                for name, data in scraped_data.items():
                    data['name'] = name
                    cpu = CPU(**data)
                    r_scores = compute_R_score(cpu,task='a')
                
                    cpu.value_score = float(cpu.multithreaded_score)/float(cpu.price) 
                    cpu.productivity_score = r_scores['p']
                    cpu.gaming_score = r_scores['g']
                    cpu.blend_score = r_scores['b']
                    cpu.save()

            if not number_of_gpus:
                logger.info('No gpus in the database. Populating beginning...')
                scraper = PassmarkScraper("gpu")
                scraped_data = scraper.get_data()

                #Stubbed functionality for calculating scores
                for name, data in scraped_data.items():
                    data['name'] = name
                    data['gaming_score'] = 0
                    data['productivity_score'] = 0
                    data['blend_score'] = 0
                    data['value_score'] = 0

                    gpu = GPU(**data)
                    gpu.save()

                