import requests
import os
import schedule
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from csv import writer


BASE_DIR = os.path.dirname(__file__)

STOCK_FILE = os.path.join(BASE_DIR, 'Stock_Codes.csv')
DF = pd.read_csv(STOCK_FILE, index_col='StockCode')

URL = 'https://www.stockbiz.vn/Stocks/'# VCB/Overview.aspx'


def get_data(response):
    date = datetime.today().strftime('%Y-%m-%d')

    soup = BeautifulSoup(response, 'lxml')
    close_price_tab = soup.find('div', class_ = 'sectionQuoteShort')
    close_price = close_price_tab.find('span', quote = 'L').text

    open_price_tab = soup.find('div', id = 'sectionQuoteDetailLeft')
    open_price = open_price_tab.find('span', quote='O').text

    price_tab = soup.find('div', id = 'sectionQuoteDetailCenter')
    high_price = price_tab.find('span', quote='HI').text
    low_price = price_tab.find('span', quote='LO').text

    change_price_tab = soup.find('div', class_ = 'sectionChangeShort')
    change_price = change_price_tab.find('span', quote='P').text

    volume_tab = soup.find('div', id = 'sectionQuoteDetailCenter2')
    volume = volume_tab.find('span', quote='TV').text

    data = f"{date}, {close_price}, {open_price}, {high_price}, {low_price}, {change_price}, {volume}"

    return data


def get_stock_data():
    for stock in DF.index:
        file_name = f"{stock}_data.csv"
        file_path = os.path.join(BASE_DIR, file_name)        

        response = requests.get(URL + f'{stock}/Overview.aspx').text
        data = get_data(response)

        if os.path.exists(file_path):
            with open(file_path, 'a') as f:
                writer_obj = writer(f)
                writer_obj.writerow(data)
        else:
            with open(file_path, 'w') as f:
                writer_obj = writer(f)
                writer_obj.writerow(['Date', 'Close', 'Open', 'High', 'Low', 'Change', 'Volume'])
                writer_obj.writerow(data)

        results.to_csv(file_path)

        
if __name__ == '__main__':

    get_stock_data()
    
    #schedule.every().day.at("15:30").do(get_info())
    
    #while 1:
    #    schedule.run_pending()
    #    time.sleep(1)