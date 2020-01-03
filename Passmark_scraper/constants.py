from os import getcwd
from os.path import join
'''
Constant values such as URLs and static values can be placed and modified here
'''

base_directory = getcwd()
passmark_base_url = 'https://www.cpubenchmark.net/'
high_end_cpus = 'https://www.cpubenchmark.net/high_end_cpus.html'
high_mid_end_cpus = 'https://www.cpubenchmark.net/mid_range_cpus.html'
low_mid_range_cpus = 'https://www.cpubenchmark.net/midlow_range_cpus.html'
low_end_cpus = 'https://www.cpubenchmark.net/low_end_cpus.html'
common_cpus = 'https://www.cpubenchmark.net/common_cpus.html'
passmark_filename = 'cpu_data.json'
passmark_log_directory = join(base_directory, 'logs', 'Passmark_scraper')


timeout_threshold = 60
time_increment = 2