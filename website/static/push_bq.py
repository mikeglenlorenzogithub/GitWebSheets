import os
import pandas as pd
# from pandas.io import gbq

from website.static.get_sheets import get_sheets

def push_bq(sheet_name):
    sheet = get_sheets('reporting.json', 'REPORTING', f'Report_{sheet_name}')
    df = pd.DataFrame(sheet.get_all_records())

    project_id = "glass-world-403808"
    dataset_id = "scrapingdata"
    table_id = 'scrapingtry'

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'access_bq_scraping.json'

    temp_df = df.copy(deep=True).replace('','null')

    temp_df[['lat', 'lon']] = temp_df[['lat', 'lon']].astype(str)
    temp_df = temp_df[['url_store', 'store_name', 'brand', 'address', 'tel_no',
                    'lat', 'lon', 'open_hours', 'holiday', 'parking', 'smoking',
                    'additional_info1', 'additional_info2', 'scrape_date']]

    temp_df.to_gbq(destination_table=f'{dataset_id}.{table_id}',
            project_id=project_id,
            if_exists='append')