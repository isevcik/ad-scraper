import scrapy
import json
import time
from datetime import datetime

class BazosSpider(scrapy.Spider):
    name = "bazos_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'bazosrealityspider.JsonWriterPipeline': 300,
        },
        "DEPTH_LIMIT": 2,
    }

    def definitions_to_start_requests(self, definitions):
        for query, params in definitions.items():
            # hledat = params["hledat"]
            # cenado = params["cenado"]
            for hlokalita in params["hlokalita"]:
                url = self.url.format(hlokalita=hlokalita);
                yield scrapy.Request(url=url, dont_filter=True)

    def start_requests(self):
        return self.definitions_to_start_requests(self.definitions)

    def parse(self, response):
        ITEM_SELECTOR = "div.inzeraty.inzeratyflex"

        for item in response.css(ITEM_SELECTOR):
            link = item.css("a::attr(href)").get()
            link = f"https://reality.bazos.cz{link}"
            date = item.css(".velikost10::text").re_first(r"(?<=\[)(.*)(?=\])")
            date = datetime.strptime(date, "%d.%m. %Y").timestamp()

            yield {
                "link": link,
                "name": item.css(".nadpis a::text").get(),
                "desc": item.css(".popis::text").get(),
                "price": item.css(".inzeratycena b::text").get(),
                "date": date,
                "img": item.css("img::attr(src)").get(),
                "raw": item.get(),
            }

            # self.logger.info("hello")
            next_page = response.css(".strankovani a:last-child")
            if next_page.css("b::text").get() == "Další":
                next_page = next_page.css("a::attr(href)").get();
                yield response.follow(next_page, self.parse)

class JsonWriterPipeline(object):
    items = {}

    def open_spider(self, spider):
        try:
            with open(spider.jsonfile,"r") as f:
                self.items = json.load(f)
        except FileNotFoundError as _:
            pass

    def close_spider(self, spider):
        with open(spider.jsonfile,"w+") as f:
            json.dump(self.items, f, sort_keys=True, indent=4, separators=(',', ': '))

    def process_item(self, item, spider):
        if item["link"] not in self.items:
            item["time"] = time.time()
            self.items[item["link"]] = item

