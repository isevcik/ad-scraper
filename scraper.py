import scrapy
import json
import time

class BazosSpider(scrapy.Spider):
    name = "bazos_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'scraper.JsonWriterPipeline': 300,
        }
    }
    start_urls = [
        "https://www.bazos.cz/search.php?hledat=keg&rubriky=www&hlokalita=60200&humkreis=25&cenaod=&cenado=&kitx=ano"
    ]

    def parse(self, response):
        ITEM_SELECTOR = "table[class=inzeraty]"
        for item in response.css(ITEM_SELECTOR):
            yield {
                "link": item.css("a::attr(href)").extract_first(),
                "name": item.css(".nadpis").extract_first(),
                "desc": item.css(".popis").extract_first()
            }

class JsonWriterPipeline(object):
    items = {}

    def open_spider(self, spider):
        try:
            with open("bazos.json","r") as f:
                self.items = json.load(f)
        except FileNotFoundError as _:
            pass

    def close_spider(self, spider):
        with open("bazos.json","w+") as f:
            json.dump(self.items, f, sort_keys=True, indent=4, separators=(',', ': '))

    def process_item(self, item, spider):
        if item["link"] not in self.items:
            item["time"] = time.time()
        self.items[item["link"]] = item