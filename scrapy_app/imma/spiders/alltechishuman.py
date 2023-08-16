import scrapy
import json
import pprint
from scrapy_splash import SplashRequest
from scrapy import Request


class AlltechishumanSpider(scrapy.Spider):
    name = "alltechishuman"
    allowed_domains = ["airtable.com"]
    handle_httpstatus_list = [401]

    start_urls = [
        "https://airtable.com/v0.3/view/viwXKKaGXCqXsTrqq/readSharedViewData?stringifiedObjectParams=%7B%22shouldUseNestedResponseFormat%22%3Atrue%7D&requestId=reqEIhFaR7ASHBMJ9&accessPolicy=%7B%22allowedActions%22%3A%5B%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viwXKKaGXCqXsTrqq%22%2C%22action%22%3A%22readSharedViewData%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viwXKKaGXCqXsTrqq%22%2C%22action%22%3A%22getMetadataForPrinting%22%7D%2C%7B%22modelClassName%22%3A%22view%22%2C%22modelIdSelector%22%3A%22viwXKKaGXCqXsTrqq%22%2C%22action%22%3A%22readSignedAttachmentUrls%22%7D%2C%7B%22modelClassName%22%3A%22row%22%2C%22modelIdSelector%22%3A%22rows%20*%5BdisplayedInView%3DviwXKKaGXCqXsTrqq%5D%22%2C%22action%22%3A%22createDocumentPreviewSession%22%7D%5D%2C%22shareId%22%3A%22shr4JVneaGOFXejUj%22%2C%22applicationId%22%3A%22apprdsx9uO4l5FieL%22%2C%22generationNumber%22%3A0%2C%22expires%22%3A%222023-08-17T00%3A00%3A00.000Z%22%2C%22signature%22%3A%22170dfea4acddc8811c8dc834bbd1b6211887ed6a91cd5fa60295494afcb2dcae%22%7D"
    ]

    headers = {
        "authority": "airtable.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,es-US;q=0.8,es;q=0.7",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google Chrome\";v=\"114\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "x-airtable-accept-msgpack": "true",
        "x-airtable-application-id": "apprdsx9uO4l5FieL",
        "x-airtable-inter-service-client": "webClient",
        "x-airtable-page-load-id": "pglFi3kBqk6mNZJLh",
        "x-early-prefetch": "true",
        "x-requested-with": "XMLHttpRequest",
        "x-time-zone": "Africa/Lagos",
        "x-user-locale": "en"
    }

    cookies = {
        "brw": "brwoWidmj2bX4Uj6s",
        "__Host-airtable-session": "eyJzZXNzaW9uSWQiOiJzZXNpaHZ5dzFzd3Q2NjZaciIsImNzcmZTZWNyZXQiOiJNbFJvTFVmalB0TjY4M1h6Q2E0TGhFRE0ifQ==",
        "__Host-airtable-session.sig": "MFe8PGof3qB4Riyxz4wRw9LsfJv_wfiZTc0_x8-XUiI",
        "_gcl_au": "1.1.397094004.1688739842",
        "_mkto_trk": "id:458-JHQ-131&token:_mch-airtable.com-1688739841923-64231",
        "_uetvid": "ebbffde01cd111ee9d0c891d050baf77",
        "_ga": "GA1.2.271267481.1688739842",
        "_ga_VJY8J9RFZM": "GS1.1.1688739842.1.1.1688739960.0.0.0",
        "_ga_H59XFK8PRM": "GS1.1.1688739844.1.1.1688739960.0.0.0",
        "AWSALB": "BZbTb5viYk9FW4xj5n0UK1YAmdXi9Z5LUXayFSF8p3hG1c69/a38h+zHDVUQWnitrtH88lSJURjgtsm9MUag6kb1VwM+HMyTGCM7aC8OFkf0dr6dJFpqaPGg6+o3",
        "AWSALBCORS": "BZbTb5viYk9FW4xj5n0UK1YAmdXi9Z5LUXayFSF8p3hG1c69/a38h+zHDVUQWnitrtH88lSJURjgtsm9MUag6kb1VwM+HMyTGCM7aC8OFkf0dr6dJFpqaPGg6+o3"
    }

    def parse(self, response):
        # Parse the JSON response
        data = json.loads(response.text)

        # Convert data to string
        data_str = json.dumps(data)

        # Check if 'data' key exists in the top-level dictionary
        if 'data' in data_str:
            # Extract the 'data' dictionary
            data_dict = data['data']

            # Check if 'rows' key exists in the 'data' dictionary
            if 'rows' in data_dict:
                rows = data_dict['rows']

                for row in rows:
                    job_id = row['id']
                    cell_values = row.get('cellValuesByColumnId', {})

                    job_title = cell_values.get('fldkaGMMS0H9Z2If6', '')
                    organization = cell_values.get('fldz1XEFevi1rTvUB', '')
                    location = cell_values.get('fldCo4yfCJrFlwnfW', '')

                    yield {
                        'job_id': job_id,
                        'job_title': job_title,
                        'organization': organization,
                        'location': location,
                    }
            else:
                self.logger.error("'rows' key not found in the JSON response.")
        else:
            self.logger.error("'data' key not found in the JSON response.")
