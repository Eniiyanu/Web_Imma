import scrapy

class ginSpider(scrapy.Spider):
    name = "giin_jobs"
    start_urls = ["https://jobs.thegiin.org/?status=contract"]

    def parse(self, response):
        job_listings = response.css('li.post.block-link')

        for job in job_listings:
            title = job.css('h5 a.block-link-src::text').get()
            company_name = job.css('p span.organization::text').get()
            job_link = response.urljoin(job.css('h5 a.block-link-src::attr(href)').get())
            date_posted = job.css('p span.posted span.new::text').get()

            yield scrapy.Request(job_link, callback=self.parse_job_details, 
                                 cb_kwargs={'title': title, 'company_name': company_name,
                                            'date_posted': date_posted})

    def parse_job_details(self, response, title, company_name, date_posted):
        job_description = response.css('div.content-area.has_aside main section div.content').get()
        deadline = response.css('ul.job-summary li:nth-child(4) p.date::text').get()
        apply_link = response.css('p.back-to-posts a.button.btn-secondary::attr(href)').get()

        yield {
            "Job Title": title,
            "Company Name": company_name,
            "Job Link": response.url,
            "Date Posted": date_posted,
            "Job Description": job_description,
            "Deadline": deadline,
            "Apply Link": apply_link,
        }
