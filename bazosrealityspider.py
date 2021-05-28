import scrapy
import json
import time
from datetime import datetime

class BazosSpider(scrapy.Spider):
    name = "bazos_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'bazosspider.JsonWriterPipeline': 300,
        },
        "DEPTH_LIMIT": 2,
    }

    def definitions_to_start_requests(self, definitions):
        for query, params in definitions.items():
            # hledat = params["hledat"]
            # cenado = params["cenado"]
            for hlokalita in params["hlokalita"]:
                # url = f"https://www.bazos.cz/search.php?hledat={hledat}&rubriky=www&hlokalita={hlokalita}&humkreis=25&cenaod=&cenado={cenado}&kitx=ano"
                
                # https://reality.bazos.cz/prodam/dum/?hledat=&rubriky=reality&hlokalita=68201&humkreis=30&cenaod=&cenado=&Submit=Hledat&kitx=ano
                url = f"https://reality.bazos.cz/prodam/dum/?hledat=&rubriky=reality&hlokalita={hlokalita}&humkreis=30&cenaod=&cenado=&kitx=ano"
                yield scrapy.Request(url=url, dont_filter=True)

    def start_requests(self):
        return self.definitions_to_start_requests(self.definitions)

    def parse(self, response):
        ITEM_SELECTOR = "table[class=inzeraty]"

        for item in response.css(ITEM_SELECTOR):
            link = item.css("a::attr(href)").get()
            link = f"https://reality.bazos.cz{link}"
            date = item.css(".velikost10::text").re_first(r"(?<=\[)(.*)(?=\])")
            date = datetime.strptime(date, "%d.%m. %Y").timestamp()

            yield {
                "link": link,
                "name": item.css(".nadpis a::text").get(),
                "desc": item.css(".popis::text").get(),
                "price": item.css(".cena b::text").get(),
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
