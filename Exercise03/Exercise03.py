import requests
import pandas as pd
import os
import json
import logging
import sys
import schedule
import time

URL = 'https://vietteltelecom.vn/api/get/sim'


logger = logging.getLogger("SIM_CRAWLING")
#create handler
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.WARNING)
if os.path.exists('sim_crawling.log') is False:
    open('sim_crawling.log', 'w')
file_handler = logging.FileHandler('sim_crawling.log')
file_handler.setLevel(logging.INFO)


#create formatter to handler
stdout_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(stdout_formatter)
file_handler.setFormatter(file_formatter)


#set level and add handler for logger
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)
logger.addHandler(file_handler)


def crawl_data(client_file):
    with open(client_file) as f:
        sim_format = f.read()

    sim_format = sim_format.split(',')
    founded = False
    for i in sim_format:
        page = 1

        data = {"key_search": i, "page": page, "page_size": 50, "total_record": 1, "isdn_type": 22}
        response = requests.post(URL, data=data)
        
        response = json.loads(response.text)
        data = response['data']
        
        if data == []:
            break
        page += 1
        df = pd.DataFrame(data)
        sim = df[['isdn']]
        sim.to_csv(client_file, mode='a', header=False, index=False)
        founded = True
        logger.info(str(i) + ' ' + 'crawled')
    
    if founded:      
        os.rename(client_file, client_file[:-4] + '_found.csv')

def crawl_sim():
    if os.path.exists('Client'):
        files = os.listdir('Client')
        files = [('Client/' + i) for i in files if i[-10:] != '_found.csv']
        print(files)
        for i in files:
            crawl_data(i)

if __name__ == '__main__':
    schedule.every().day.at("15:00").do(crawl_sim)
    while True:
        schedule.run_pending()
        time.sleep(1)