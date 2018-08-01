import scrapy

from ..items import Job

DOMAIN = "https://remotelist.io"

class RemoteListIoSpider(scrapy.Spider):
    """ This class crawls the remote jobs in remotelist """

    name = "remotelistio"
    def start_requests(self):
        urls = [
            'https://remotelist.io/'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jobs = []
        
        for row in response.css("tr.row"):
            job = Job()
            job["url"] = DOMAIN + row.css("td")[0].css("div::attr(data-url)").extract_first()
            job["position"] = row.css("td")[0].css("strong::text").extract_first()
            job["company"] = row.css("td")[1].css("a::text").extract_first()
            job["tags"] = row.css("td")[2].css("a::text").extract()
            job["date"] = row.css("td")[3].css("span::text").extract_first().strip()

            jobs.append(job)
        
        return jobs