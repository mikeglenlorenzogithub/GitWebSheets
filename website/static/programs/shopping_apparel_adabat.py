from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import time
import pendulum
import re
from fake_useragent import UserAgent
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from website.static.get_sheets import get_sheets

class ShoppingApparelAdabat():
    def __init__(self):
        self.session = requests.Session()
        self.session_html = HTMLSession()
        # retry = Retry(connect=3, backoff_factor=0.5)
        # adapter = HTTPAdapter(max_retries=retry)
        # self.session.mount('http://', adapter)
        # self.session.mount('https://', adapter)

        self.content = []
        self.file_name = 'shopping_apparel_adabat'

        start = time.time()
        self.get_data()
        end = time.time()

        print("============ ", (end - start) / 60, " minute(s) ============")
        
        x = pd.DataFrame(self.content)

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

            try:
                self.report.insert_row([self.file_name, x['scrape_date'][0], 'Datanya Lolos checking'], len(self.report.get_all_records())+2)
            except:
                print('REACH LIMIT!, REST A LITTLE BIT')
                time.sleep(60)
                self.report = get_sheets('reporting.json', 'REPORTING', 'Report')
                self.report.insert_row([self.file_name, x['scrape_date'][0], 'Datanya Lolos checking'], len(self.report.get_all_records())+2)
                print('CONTINUE')

            print('Datanya Lolos checking... ✔')

        except:
            x.to_csv(f'{self.file_name}.csv', index=False)
            self.report.insert_row([self.file_name, x['scrape_date'][0], 'Datanya masih blm bersih tolong di cek ulang!!! ❌'], len(self.report.get_all_records())+2)
            print('Datanya masih blm bersih tolong di cek ulang!!! ❌')
            raise
    
    def get_data(self):
        url = "https://store.world.co.jp/real-store-search?pref=&br=BR082&pcf=1&so=1%2C3&page=1"
        headers = {'user-agent':UserAgent().random}
        req = self.session_html.get(url, headers=headers)

        #request.html.render(timeout=0)
    
        while True:
            soup = BeautifulSoup(req.html.html, 'html.parser')
            stores = soup.select('li.point')
            for store in stores:
                store_name = " ".join(store.find('div','txt_shop-name').get_text(strip=True, separator=' ').split())
                url_store = store.find('a')['href']
    
                information = store.find('div','txt_address').get_text(strip=True, separator=' ').split()
                address = " ".join(information[:-1]).strip()
                tel_no = information[-1].strip()
                open_hours = ""
    
                # url_map = f"http://www.google.com/maps/search/{address}{chain_name}{store_name}"
                # req_map = self.s.get(url_map, allow_redirects=True)
                # location = req_map.html.find('meta[property="og:image"]', first=True).attrs['content']
                # try:
                #     lat_lon = location.split('&markers=')[1].split('%7C')[0].split('%2C')
                #     lat, lon = lat_lon[0], lat_lon[1]
                # except:
                #     lat_lon = location.split('center=')[1].split('&zoom')[0].split('%2C')
                #     lat, lon = lat_lon[0], lat_lon[1]
                while True:
                    try:
                        req2 = self.session_html.get(url_store, headers=headers)
                        break
                    except:
                        print('TERJADI PERULANGAN req2!!!')
                        time.sleep(2)

                location = 'script:contains("latlng")'
                lat_lon = req2.html.find(location, first=True).text.split('LatLng(')[1].split(');')[0].split(',')
                lat, lon = lat_lon[0].strip(), lat_lon[1].strip()

                self.save_data(url_store, store_name, address, tel_no, lat, lon)

            if soup.select_one('li[class="search-result__paging__last"] a'):
                url = soup.select_one('li[class="search-result__paging__last"] a')['href']
                req = self.session_html.get(url, headers=headers)
            else:
                break

    def save_data(self, url_store, store_name, address, tel_no, lat, lon):
        data_dict = dict()
        data_dict['url_store'] = url_store
        data_dict['store_name'] = store_name
        data_dict['brand'] = "adabat"
        data_dict['address'] = address
        data_dict['tel_no'] = tel_no
        data_dict['lat'] = lat
        data_dict['lon'] = lon
        data_dict['open_hours'] = ''
        data_dict['holiday'] = ''
        data_dict['parking'] = ''
        data_dict['smoking'] = ''
        data_dict['additional_info1'] = ''
        data_dict['additional_info2'] = ''
        
        utc_time = pendulum.now()
        indonesia = utc_time.in_timezone('Asia/Bangkok')
        data_dict["scrape_date"] = indonesia.strftime("%m/%d/%y")

        self.content.append(data_dict)
        print(len(self.content), url_store)

if __name__ == '__main__':
    ShoppingApparelAdabat()