from fake_useragent import UserAgent
from datetime import date
import time
from bs4 import BeautifulSoup
import pendulum
from requests_html import HTMLSession, AsyncHTMLSession
import pyppeteer
import pandas as pd
import re

from website.static.get_sheets import get_sheets

class ShoppingApparelAdametrope():

    def __init__(self, from_main=False):
        self.from_main = from_main
        self.rand_agent = {'user-agent': UserAgent().random}
        self.content = list()
        self.s = HTMLSession()
        self.content = []
        self.start_time = time.time()
        self.get_data()

        print('--- %s minutes ---' % ((time.time() - self.start_time) / 60))

        x = pd.DataFrame(self.content)
        if len(x) == 0:
            raise ValueError('Isinya ra ono.')
        
        self.file_name = 'shopping_apparel_adametrope'

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
        # url = 'https://www.adametrope.com/shoplist?_gl=1*gebjch*_ga*NzQ0NDgwMjQ5LjE2Mzg1MjQzMDE.*_ga_Y173CWX5CZ*MTYzODUyNDMwMC4xLjEuMTYzODUyNDMxMy4w&_ga=2.252841418.2121798017.1638524301-744480249.1638524301'
        url = 'https://www.adametrope.com/shoplist?'
        req = self.s.get(url, headers=self.rand_agent)
        soup = BeautifulSoup(req.content, 'html.parser')
        cards = soup.findAll('article', 'column')
        for card in cards:
            store_name = card.find('h2').text.strip().replace('\r\n', ' ')
            address = card.find('ul').findAll('li')[0].text.strip().split('\r\n')[0]
            tel_no = card.find('ul').findAll('li')[1].text.replace('Tel.', '').replace('※店舗通販可能','').strip().replace('ｔel','').replace('.','')
            open_hours = card.find('ul').findAll('li')[2].text.strip()
            url_map = f"http://www.google.com/maps/search/{' '.join(address.split())}"
            req_map = self.s.get(url_map, allow_redirects=True)
            location = req_map.html.find('meta[property="og:image"]', first=True).attrs['content']
            try:
                lat_lon = location.split('&markers=')[1].split('%7C')[0].split('%2C')
                lat, lon = lat_lon[0], lat_lon[1]
            except:
                lat_lon = location.split('center=')[1].split('&zoom')[0].split('%2C')
                lat, lon = lat_lon[0], lat_lon[1]
            
            self.save_data(url, store_name, address, tel_no, open_hours, lat, lon)

    def save_data(self, url_store, store_name, address, tel_no, open_hours, lat, lon):
        data_dict = dict()
        data_dict['url_store'] = url_store
        data_dict['store_name'] = store_name
        data_dict['brand'] = 'ADAM ET ROPE'
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
    ShoppingApparelAdametrope(True)