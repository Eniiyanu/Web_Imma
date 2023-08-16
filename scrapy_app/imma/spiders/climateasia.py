import scrapy
import json

class caSpider(scrapy.Spider):
    name = 'climateasia'
    start_urls = ['https://api.climateasia.org/api/jobs?keyword=consultant']

    def parse(self, response):
        data = json.loads(response.text)
        jobs = data['body']['all_jobs']
        
        for job in jobs:
            job_title = job['title']
            company = job['external_company_name']
            date_created = job['fmt_created_at']
            #location = job['job_location'][0]['city_brief']['name']
            job_url = job['job_link']
            
            yield scrapy.Request(job_url, callback=self.parse_job_details, meta={
                'Job Title': job_title,
                'Company': company,
                'Date Created': date_created,
                #'Location': location,
                'Job URL': job_url
            })

    def parse_job_details(self, response):
        job_title = response.meta['Job Title']
        company = response.meta['Company']
        date_created = response.meta['Date Created']
        #location = response.meta['Location']
        job_url = response.meta['Job URL']
        description = response.css('.job-description::text').get()

        yield {
            'Job Title': job_title,
            'Company': company,
            'Date Created': date_created,
            #'Location': location,
            'Job URL': job_url,
            'Description': description
        }
