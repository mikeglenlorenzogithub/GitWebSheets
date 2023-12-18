from fake_useragent import UserAgent
import datetime, time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import re
import pendulum

from website.static.get_sheets import get_sheets

class ShoppingApparelBape():

    def __init__(self, from_main=False):
        self.from_main = from_main
 
        self.file_name = 'shopping/apparel/bape'.replace("/", "_")
        self.content = list()
        self.session = HTMLSession()
        self.start = time.time()

        self.url = 'https://bape.com/pages/store-list/'

        self.get_page(self.url)
        self.end = time.time()

        print(f'--- {(self.end - self.start)/60} minutes ---')
        
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

    def get_page(self, url):
        """
  Visit the link given from the gsheet,
  see if there's data there.
  If yes, scrape immediately.
  If no, call get_data(self.url) and visit individual pages.
  """
        headers = {'user-agent': UserAgent().random.strip()}
        page = self.session.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        cards = ' '.join(soup.select_one('div#shopify-section-store-list script').text.split()).split('window.args.storeList.dealers.push')[0].split('window.args.storeList.stores.push')

        for card in cards[1:len(cards)]:
            # print(card)
            url_store = 'https://bape.com/pages/store-list/' + card.split('handle: "')[1].split('", name')[0]

            store_name = ' '.join(card.split('name: "')[1].split('", address')[0].replace('BAPE ','').replace('BAPE','').replace('®','').replace('™','').split('", nameEn:')[0].split())
            if '\/' in store_name:
                store_name = ' '.join(store_name.replace('\\','').split())
            address = card.split('address: "')[1].split('", phone')[0].split('", addressEn')[0]
            tel_no = card.split('phone: "')[1].split('", openingHours')[0]
            open_hours = card.split('openingHours: "')[1].split('", location')[0].replace('\\n',' ')
            
            if '〒' not in address:
                continue

            lat_lon = card.split('latitude:')[1].split(', }, imagesUrls')[0].replace(' ','').replace('longitude:','').split(',')
            lat = lat_lon[0]
            lon = lat_lon[1]

            data_dict = dict()
            data_dict['url_store'] = url_store
            data_dict['store_name'] = store_name
            data_dict['chain_name'] = 'BAPE'
            data_dict['CSAR_Category'] = 'SS'
            data_dict['chain_id'] = 'shopping/apparel/bape'
            data_dict['e_chain'] = 'BAPE'
            data_dict['categories'] = 'apparel'
            data_dict['業種大'] = 'ショッピング'
            data_dict['業種中'] = 'アパレル'
            data_dict['address'] = address
            data_dict['lat'] = lat
            data_dict['lon'] = lon
            data_dict['tel_no'] = tel_no
            data_dict['営業時間'] = open_hours
            data_dict['gla'] = ''

            utc_time = pendulum.now()
            indonesia = utc_time.in_timezone('Asia/Bangkok')
            data_dict["scrape_date"] = indonesia.strftime('%m/%d/%y')

            self.content.append(data_dict)
            print(len(self.content), url_store)

        self.save_data()

    def save_data(self):
        if self.from_main:
            df = pd.DataFrame(self.content)
            df = df.reindex(columns=['store_name', 'chain_name', 'CSAR_Category', 'chain_id', 'e_chain', 'categories', '業種大', '業種中', 'address', 'url_store', 'url_tenant', '営業時間', '定休日', '駐車場', '禁煙・喫煙', '取扱', '備考', 'lat', 'lon', 'tel_no', 'gla', 'scrape_date'])
          
if __name__ == '__main__':
    ShoppingApparelBape(True)