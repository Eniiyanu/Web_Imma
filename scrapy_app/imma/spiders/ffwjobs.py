import scrapy
import json

class ffwSpider(scrapy.Spider):
    name = 'ffwjobs'
    start_urls = ['https://jobs.ffwd.org/api/search/jobs?networkId=997&hitsPerPage=20&page=1&filters=&query=']

    def parse(self, response):
        data = json.loads(response.text)
        results = data['results'][0]['hits']
        
        for result in results:
            job_title = result['title']
            company = result['organization']['name']
            date_created = result['created_at']
            location = result['locations']
            
            yield {
                'Job Title': job_title,
                'Company': company,
                'Date Created': date_created,
                'Location': location
            }
        
        # Check if there are more pages to load
        if data.get('nbPages', 0) > 1:
            next_page = response.urljoin(f'&page={data["page"] + 1}')
            yield scrapy.Request(next_page, callback=self.parse)
