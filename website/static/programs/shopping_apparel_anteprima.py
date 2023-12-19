import asyncio
from fake_useragent import UserAgent
import datetime, time
from bs4 import BeautifulSoup
from requests_html import HTMLSession, AsyncHTMLSession
import pyppeteer
import pandas as pd
import re
import pendulum

from website.static.get_sheets import get_sheets

class ShoppingApparelAnteprima():

    def __init__(self, from_main=False):
        self.from_main = from_main
 
        self.file_name = 'shopping/apparel/anteprima'.replace("/", "_")
        self.content = []

        self.session = HTMLSession()
        self.start = time.time()
        self.get_data()
        self.end = time.time()
        
        print("--- %s minutes ---" % ((self.end - self.start)/60))

        x = pd.DataFrame(self.content)
        if len(x) == 0:
            raise ValueError('Isinya ra ono.')
        
        # CLEANING 1: PERIKSA KOORDINAT
        # x['lat'] = pd.to_numeric(x['lat'], errors='coerce')
        # x['lon'] = pd.to_numeric(x['lon'], errors='coerce')
        # x.loc[x[(x['lat'] < 20) | (x['lat'] > 50)].index, 'lat'] = pd.NA
        # x.loc[x[(x['lat'] < 20) | (x['lat'] > 50)].index, 'lon'] = pd.NA

        # x.loc[x[(x['lon'] < 121) | (x['lon'] > 154)].index, 'lat'] = pd.NA
        # x.loc[x[(x['lon'] < 121) | (x['lon'] > 154)].index, 'lon'] = pd.NA

        self.report = get_sheets('reporting.json', 'REPORTING', 'Report')
        if self.report.cell(1,1).value == '' or self.report.cell(1,1).value == None:
            self.report.insert_row(['File Name', 'Scrape Date', 'Status'], 1)
        else:
            pass

        try:
            x['tuple_result'] = x[list(x.columns)].apply(tuple, axis=1)

            sheet = get_sheets('reporting.json', 'REPORTING', f'Report_{self.file_name}')
            try:
                sheet.delete_rows(1,len(sheet.get_all_records())+1)
            except:
                print('EMPTY SHEET!')
                pass
            sheet.insert_row(list(x.columns), 1)
            for row in x['tuple_result']:
                try:
                    sheet.insert_row(row, len(sheet.get_all_records())+2)
                except:
                    print('REACH LIMIT!, REST A LITTLE BIT')
                    time.sleep(60)
                    sheet = get_sheets('reporting.json', 'REPORTING', f'Report_{self.file_name}')
                    sheet.insert_row(row, len(sheet.get_all_records())+2)
                    print('CONTINUE')

            self.report.insert_row([self.file_name, x['scrape_date'][0], 'Datanya Lolos checking'], len(self.report.get_all_records())+2)
            print('Datanya Lolos checking... ✔')

        except:
            x.to_csv(f'{self.file_name}.csv', index=False)
            self.report.insert_row([self.file_name, x['scrape_date'][0], 'Datanya masih blm bersih tolong di cek ulang!!! ❌'], len(self.report.get_all_records())+2)
            print('Datanya masih blm bersih tolong di cek ulang!!! ❌')
            raise

    def get_data(self):
        """
  Visit individual page,
  see if you can scrape map latitude and longitude.
  If no, visit map individually by calling get_map_data(self.url)
  """
        url = 'https://jp.anteprima.com/shop_list/locationlist/loc:jp/'
        req = self.session.get(url, headers={'user-agent':UserAgent().random})
        soup = BeautifulSoup(req.html.html, 'html.parser')
        
        i = 0
        cards = soup.select('h5 a')
        for card in cards:
            i += 1
            data_dict = dict()
            url_store = 'https://jp.anteprima.com'+card.get('href')

            data_dict['url_store'] = url_store
            while True:
                try:
                    req2 = self.session.get(url_store, headers={'user-agent':UserAgent().random.strip()})
                    soup2 = BeautifulSoup(req2.html.html, 'html.parser')
                    soup2.select_one('#stores_detail h3').text
                    break
                except (TypeError, AttributeError):
                    print('TERJADI PERULANGAN req2!!!')
                    time.sleep(3)
            
            store_name = soup2.select_one('#stores_detail h3').text
            address = soup2.select_one('#stores_access section p').text
            try:
                tel_no = ' '.join(soup2.select_one('#stores_info td.tel').text.split())
                tel_no = tel_no.replace(' ','-')
            except:
                tel_no = soup2.select_one('#stores_info td.tel').text.split()
                tel_no = tel_no.replace(' ','-')

            tel_no = tel_no.replace('（代表）','').replace('（大代表）','')
            open_hours = ''
            lat = ''
            lon = ''

            self.save_data(url_store, store_name, address, tel_no, open_hours, lat, lon)

    def save_data(self, url_store, store_name, address, tel_no, open_hours, lat, lon):
        data_dict = dict()
        data_dict['url_store'] = url_store
        data_dict['store_name'] = store_name
        data_dict['brand'] = 'ANTEPRIMA'
        data_dict['address'] = address
        data_dict['tel_no'] = tel_no
        data_dict['lat'] = lat
        data_dict['lon'] = lon
        data_dict['open_hours'] = open_hours
        data_dict['holiday'] = ''
        data_dict['parking'] = ''
        data_dict['smoking'] = ''
        data_dict['additional_info1'] = ''
        data_dict['additional_info2'] = ''

        utc_time = pendulum.now()
        indonesia = utc_time.in_timezone('Asia/Bangkok')
        data_dict['scrape_date'] = indonesia.strftime('%m/%d/%Y')

        self.content.append(data_dict)
        print(len(self.content), url_store)

if __name__ == '__main__':
    ShoppingApparelAnteprima(True)