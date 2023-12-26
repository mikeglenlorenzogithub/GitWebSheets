# GitWebSheets
web app to get data from web (scrape or even crawl) and put the data in spreadsheet using API

On the way to make some choices, run all or one by one

1. create venv, if failed to activate try Set-ExecutionPolicy Unrestricted -Scope Process

cheat setting
runtime_config:
    python_version: 3

manual_scaling:
    instances: 1

resources:
    cpu: 1
    memory_gb: 0.5
    disk_size_gb: 10

# QUERY CONVERT STRING TO DATE
BEGIN TRANSACTION;

UPDATE `glass-world-403808.scrapingdata.scraping_convert`
SET scrape_date = '2023-12-25'
WHERE scrape_date = '12/25/23';

UPDATE `glass-world-403808.scrapingdata.scraping_convert`
SET scrape_date = '2023-12-25'
WHERE scrape_date = '12/25/2023';

SELECT CAST(scrape_date AS DATE) FROM `glass-world-403808.scrapingdata.scraping_convert`;

SELECT scrape_date FROM `glass-world-403808.scrapingdata.scraping_convert`;

ROLLBACK TRANSACTION;
-- COMMIT TRANSACTION;