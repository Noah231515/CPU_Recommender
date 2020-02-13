from os import getcwd
from os.path import join
'''
Constant values such as URLs and static values can be placed and modified here
'''

base_directory = getcwd()
passmark_log_directory = join(base_directory, 'logs', 'passmark_scraper')
passmark_base_url='https://www.cpubenchmark.net/'
passmark_base_url_gpu='https://www.videocardbenchmark.net/'
high_end_cpus='https://www.cpubenchmark.net/high_end_cpus.html'
high_mid_end_cpus='https://www.cpubenchmark.net/mid_range_cpus.html'
low_mid_range_cpus='https://www.cpubenchmark.net/midlow_range_cpus.html'
low_end_cpus='https://www.cpubenchmark.net/low_end_cpus.html'
common_cpus='https://www.cpubenchmark.net/common_cpus.html'
high_end_gpus='https://www.videocardbenchmark.net/high_end_gpus.html'
common_gpus='https://www.videocardbenchmark.net/common_gpus.html'
passmark_filename='cpu_data.json'
google_images='https://www.google.com/search?safe=off&hl=en&tbm=isch'

part_urls = {
    'cpu': [high_end_cpus, common_cpus],
    'gpu': [high_end_gpus, common_gpus],
    
}
regex_strings={ #contains reusable regex patterns
    'blah': 'blah',
    'class': '({REPLACE_ME}:\s+)(\S+)',
    'generic_value': '({REPLACE_ME}:\s*)(\d+)',
    'release_date': '({REPLACE_ME}:\s*)(Q\d+\s\d+)',
    'score': '({REPLACE_ME})(\n \d+)',
    'samples': '(Samples:\s*)(\d+)',
    'price': '\$((\d+[,.])*(\d+))',
}
timeout_threshold = 60
time_increment = 2