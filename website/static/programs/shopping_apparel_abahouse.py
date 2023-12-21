from fake_useragent import UserAgent
import datetime, time
from bs4 import BeautifulSoup
# IMPORT PENTING
from requests_html import HTMLSession
import pandas as pd
import re
import pendulum

from website.static.get_sheets import get_sheets

class ShoppingApparelAbahouse():
    def __init__(self):
        self.session = HTMLSession()
        self.content = list()
        self.file_name = 'shopping/apparel/abahouse'.replace('/','_')
        start = time.time()
        url = "https://abahouse.co.jp/shop-search/?&brand=ABAHOUSE"
        self.get_page(url)
        end = time.time()
        print("============ ", (end - start)/60, " minute(s) ============")

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
        
    def get_page(self, url):
        headers = {'user-agent': UserAgent().random.strip()}
        page = self.session.get(url, headers=headers)
        soup = BeautifulSoup(page.html.html, 'html.parser')

        store_lists = soup.select('table.cellContent')
        for store in store_lists:
            if store.find('h2').text.startswith('アバハウス'):
                try:
                    url_store = store.find('th', string='店舗ブログ').find_next('td').find_next('a')['href']
                except:
                    url_store = page.url

                store_name = store.find('th', string='店舗名').find_next_sibling('td').text.replace(' ', '').replace('\u3000', '')
                store_name = store_name.replace('アバハウス/ルージュ・ヴィフラクレ','').replace('アバハウス/','').replace('アバハウス','')

                address = store.find('th', string='住所').find_next_sibling('td').text.replace('\n', '').replace(' ', '').replace('\u3000', '').replace('?','-')
                if not address.startswith('〒'): continue

                tel_no = store.find('th', string='電話番号').find_next_sibling('td').text

                maps_link = store.find('th', string='住所').find_next('td').select_one('li.btn a').get('href')
                req_maps = self.session.get(maps_link, headers={'user-agent': UserAgent().random.strip()})
                try:
                    try:
                        lat_lon = req_maps.url.split('/%40')[1].split('z/data=')[0].split(',')
                    except:
                        lat_lon = req_maps.url.split('/@')[1].split('z/data=')[0].split(',')
                except:
                    lat_lon = ['','']
                lat = lat_lon[0]
                lon = lat_lon[1]

                info1 = store.find('th', string='取り扱いブランド').find_next_sibling('td').text.replace('\n', '').replace(' ', '').replace('\u3000', '') # Handling

                self.save_data(url_store, store_name, address, tel_no, info1, lat, lon)
        
        try:
            next_button = "https://abahouse.co.jp/shop-search/" + soup.find('li', 'next').find('a')['href']
            self.get_page(next_button)
        except AttributeError:
            pass


    def save_data(self, url_store, store_name, address, tel_no, info1, lat, lon):
        data_dict = dict()
        data_dict['url_store'] = url_store
        data_dict['store_name'] = store_name
        data_dict['brand'] = "ABAHOUSE"
        data_dict['address'] = address
        data_dict['tel_no'] = tel_no
        data_dict['lat'] = lat
        data_dict['lon'] = lon
        data_dict['open_hours'] = ''
        data_dict['holiday'] = ''
        data_dict['parking'] = ''
        data_dict['smoking'] = ''
        data_dict['additional_info1'] = info1
        data_dict['additional_info2'] = ''

        utc_time = pendulum.now()
        indonesia = utc_time.in_timezone('Asia/Bangkok')
        data_dict["scrape_date"] = indonesia.strftime('%m/%d/%y')

        self.content.append(data_dict)

        print(len(self.content), url_store)

if __name__ == '__main__':
    ShoppingApparelAbahouse()