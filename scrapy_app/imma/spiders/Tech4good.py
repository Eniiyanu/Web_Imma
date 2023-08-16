import scrapy


class tech4goodjobs(scrapy.Spider):
    name = "tech4goodjobs"
    start_urls = ["https://tech4goodjobs.com/jobs?q=&category=&job_type=10953&location=&location_id="]

    def parse(self, response):
        job_listings = response.css('.job-listings-item')

        for listing in job_listings:
            job_title = listing.css('.job-details-link h3::text').get().strip()
            location = " ".join(listing.css('.job-details-info-item:nth-child(3) *::text').getall()).strip().replace('\n', '').replace('\r', '').replace('\t', '')

            company_name = listing.css('.job-details-info-item:nth-child(1) a::text').get().strip()
            date_posted = listing.css('div.job-posted-date::text').get().strip()
            job_link = response.urljoin(listing.css('.job-details-link::attr(href)').get())

            yield scrapy.Request(
                job_link,
                callback=self.parse_job_details,
                meta={
                    'job_title': job_title,
                    'location': location,
                    'company_name': company_name,
                    'date_posted': date_posted,
                    'job_link': job_link
                }
            )

    def parse_job_details(self, response):
        job_description = response.css('.quill-container-with-job-details ::text').getall()

        # Clean up the job description text
        job_description = ' '.join(job_description).strip()

        # Get the previously extracted data from the meta field
        job_title = response.meta['job_title']
        location = response.meta['location']
        company_name = response.meta['company_name']
        date_posted = response.meta['date_posted']
        job_link = response.meta['job_link']

        # Process the extracted data (e.g., print or store it)
        print("Job Title:", job_title)
        print("Location:", location)
        print("Company Name:", company_name)
        print("Date Posted:", date_posted)
        print("Job Link:", job_link)
        print("Job Description:", job_description)


# Run the spider
if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess(settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    })

    process.crawl(tech4goodjobs)
    process.start()








