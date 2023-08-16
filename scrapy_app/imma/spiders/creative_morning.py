import scrapy
import json

class cmSpider(scrapy.Spider):
    name = 'creative_morning'
    start_urls = ['https://creativemornings.com/jobs/_search']
    custom_settings = {
        'DOWNLOAD_DELAY': 2
    }
    base_url = 'https://creativemornings.com/jobs/_search'
    page = 0
    threshold = 10  # Set the threshold value based on the number of results per page
    keywords = ['freelance', 'part time', 'remote']  # List of keywords to filter job titles
    positions = ['consultant']  # List of job positions to filter

    def parse(self, response):
        if response.headers.get('Content-Type', b'').startswith(b'application/json'):
            data = json.loads(response.text)
            hits = data.get('hits', {}).get('hits', [])

            for hit in hits:
                job = hit.get('_source', {})
                title = job.get('title')
                company = job.get('company', {}).get('name')
                location = job.get('location')

                if self.should_yield_job(title, location):
                    yield {
                        'title': title,
                        'company': company,
                        'location': location
                    }

            self.page += 1
            if len(hits) >= self.threshold:
                yield scrapy.Request(
                    url=self.base_url,
                    method='POST',
                    body=self.get_request_body(),
                    headers={'Content-Type': 'application/json'},
                    callback=self.parse
                )
        else:
            for job in response.css('.job-item'):
                title = job.css('.title::text').get()
                company = job.css('.company::text').get()
                location = job.css('.location::text').get()

                if self.should_yield_job(title, location):
                    yield {
                        'title': title,
                        'company': company,
                        'location': location
                    }

    def get_request_body(self):
        return json.dumps({
            "query": {
                "match_all": {}
            },
            "from": self.page * 10,
            "size": 10
        })

    def should_yield_job(self, title, location):
        if title and location:
            title_lower = title.lower()
            location_lower = location.lower()

            # Check if any keyword is present in the job title
            if any(keyword in title_lower for keyword in self.keywords):
                # Check if any job position is present in the job title
                if any(position in title_lower for position in self.positions):
                    return True

            # Check if any keyword is present in the job location
            if any(keyword in location_lower for keyword in self.keywords):
                # Check if any job position is present in the job location
                if any(position in location_lower for position in self.positions):
                    return True

        return False
