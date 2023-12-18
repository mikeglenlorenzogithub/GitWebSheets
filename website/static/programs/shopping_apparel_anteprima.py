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

            data_dict['store_name'] = soup2.select_one('#stores_detail h3').text
            data_dict['chain_name'] = 'ANTEPRIMA'
            data_dict['CSAR_Category'] = 'SS'
            data_dict['chain_id'] = 'shopping/apparel/anteprima'
            data_dict['e_chain'] = 'ANTEPRIMA'
            data_dict['categories'] = 'apparel'
            data_dict['業種大'] = 'ショッピング'
            data_dict['業種中'] = 'アパレル'
            data_dict['address'] = soup2.select_one('#stores_access section p').text
            maps_link = 'https://www.google.com/maps/search/' + data_dict['address']

            data_dict['lat'], data_dict['lon'] = '', ''
            try:
                tel_no = ' '.join(soup2.select_one('#stores_info td.tel').text.split())
                tel_no = tel_no.replace(' ','-')
            except:
                tel_no = soup2.select_one('#stores_info td.tel').text.split()
                tel_no = tel_no.replace(' ','-')

            data_dict['tel_no'] = tel_no.replace('（代表）','').replace('（大代表）','')
            data_dict['営業時間'] = ''
            data_dict['gla'] = ''
            
            utc_time = pendulum.now()
            indonesia = utc_time.in_timezone('Asia/Bangkok')
            data_dict["scrape_date"] = indonesia.strftime('%m/%d/%y')
            
            if data_dict not in self.content:
                self.content.append(data_dict)
                print(len(self.content), url_store)

    def save_data(self):
        if self.from_main:
            df = pd.DataFrame(self.content)
            df = df.reindex(columns=['store_name', 'chain_name', 'CSAR_Category', 'chain_id', 'e_chain', 'categories', '業種大', '業種中', 'address', 'url_store', 'url_tenant', '営業時間', '定休日', '駐車場', '禁煙・喫煙', '取扱', '備考', 'lat', 'lon', 'tel_no', 'gla', 'scrape_date'])

if __name__ == '__main__':
    ShoppingApparelAnteprima(True)