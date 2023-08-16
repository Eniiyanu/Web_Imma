import scrapy
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from spiders.alltechishuman import AlltechishumanSpider
from spiders.climateasia import caSpider
from spiders.creative_morning import cmSpider
from spiders.ffwjobs import ffwSpider
from spiders.giin import ginSpider
from spiders.Tech4good import tech4goodjobs
from google.oauth2.service_account import Credentials
# Replace 'your_credentials.json' with the name of your downloaded credentials file
CREDENTIALS_FILE = 'C:/Users/USER/Desktop/imma_auto/imma/unique-yew-384612-7b2101afeeee.json'
SPREADSHEET_NAME = 'Web_Scraping'

# Create a dictionary to map spider names to their corresponding classes
SPIDERS = {
    'alltechishuman': AlltechishumanSpider,
    'climateasia': caSpider,
    #'creative_morning': cmSpider,
    'ffwjobs': ffwSpider,
    'giin_jobs': ginSpider,
    'tech4goodjobs': tech4goodjobs
}

# Enable logging to debug any potential issues
logging.basicConfig(level=logging.DEBUG)

def get_spreadsheet():
    # Set up Google Sheets API credentials using google-auth library
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(CREDENTIALS_FILE, scopes=scope)
    client = gspread.authorize(credentials)

    # Open the spreadsheet by name
    return client.open(SPREADSHEET_NAME)

# ... (previous code)

def update_spreadsheet(spider_data):
    logging.debug(f"data type: {type(spider_data)}")
    logging.debug(f"data content: {spider_data}")
    try:
        # Open the spreadsheet
        spreadsheet = get_spreadsheet()

        # Select the appropriate worksheet
        worksheet = spreadsheet.get_worksheet(0)

        # Clear the worksheet and update the header row
        worksheet.clear()
        worksheet.insert_row(['Spider Name', 'Job ID', 'Job Title', 'Organization', 'Location'], index=1)

        # Insert the data into the worksheet
        row_number = 2
        for spider_name, data in spider_data.items():
            logging.debug(f"Spider: {spider_name}")
            for job_data in data:
                logging.debug(f"job_data type: {type(job_data)}")
                logging.debug(f"job_data content: {job_data}")
                if not isinstance(job_data, dict):
                    logging.error(f"job_data is not a dictionary: {job_data}")
                    continue
                row_values = [spider_name, job_data.get('job_id', ''), job_data.get('job_title', ''), job_data.get('organization', ''), job_data.get('location', '')]
                worksheet.insert_row(row_values, index=row_number)
                row_number += 1
    except Exception as e:
        logging.error(f"Error updating spreadsheet: {e}")

# ... (rest of the code)



# ... (rest of the code)# ... (previous code)

def run_spiders_and_update_sheet():
    # Create a CrawlerRunner
    runner = CrawlerRunner(settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    })

    # Create an empty dictionary to store the scraped data for each spider
    spider_output = {}

    # Function to handle the spider output
    def handle_output(output, name):
        spider_output[name] = output
        logging.debug(f"Spider {name} finished. Output length: {len(output)}")

    # Function to finish when all spiders have finished running
    def finish_all(_):
        if spider_output:
            update_spreadsheet(spider_output)
            logging.debug("Spreadsheet updated.")
        else:
            logging.error("No data to update in the spreadsheet.")
        reactor.stop()

    # Create a list of deferreds for each spider
    deferred_list = [runner.crawl(spider_class) for spider_name, spider_class in SPIDERS.items()]

    # When all spiders have finished running, call the finish_all function
    d = defer.DeferredList(deferred_list)
    d.addBoth(finish_all)

    # Start the CrawlerRunner
    reactor.run()

# ... (rest of the code)

# Run the spiders and update the Google Spreadsheet
if __name__ == "__main__":
    run_spiders_and_update_sheet()
