import scrapy
import json
import time
from datetime import datetime
from pprint import pformat

class BezrealitkySpider(scrapy.Spider):
    name = "bezrealitky_spider"
    custom_settings = {
        'ITEM_PIPELINES': {
            'bezrealitkyspider.JsonWriterPipeline': 300,
        },
        "DEPTH_LIMIT": 2,
    }

    def definitions_to_start_requests(self, definitions):
        for k, v in definitions.items():
            url = v["url"]
            formdata = v["formdata"]
            yield scrapy.FormRequest(url=url, formdata=formdata, dont_filter=True)

    def start_requests(self):
        return self.definitions_to_start_requests(self.definitions)

    def parse(self, response):
        items = response.json()
        ids = list(map(lambda i: i["id"], items))
        self.logger.info("ids:")
        self.logger.info(pformat(ids))

        return self.build_graphql_request(ids)

    def parse_graphql(self, response):
        items = response.json();
        adverts = items["data"]["adverts"]["list"]
        self.logger.info("here")
        self.logger.info(pformat(items))

        for item in adverts:
            self.logger.info(pformat(item))
            link = f"https://www.bezrealitky.cz/nemovitosti-byty-domy/{item['uri']}"
            name = f"{item['shortDescription']}, {item['address']}"

            yield {
                "oid": item["id"],
                "link": link,
                "name": name,
                "desc": item['shortDescription'],
                "price": item['priceFormatted'],
                # "date": item['timeOrder']['date'],
                "img": item['mainImageUrl'],
                "raw": json.dumps(item)
            }

    def build_graphql_request(self, ids):
        data = {
            "query": "query Adverts($offerType: [OfferType], $estateType: [EstateType], $disposition: [Disposition], $ownership: [Ownership], $construction: [Construction], $equipped: [Equipped], $priceFrom: Int, $priceTo: Int, $surfaceFrom: Int, $surfaceTo: Int, $limit: Int, $offset: Int, $order: ResultOrder, $boundary: String, $ids: [Int], $locale: String!, $developer: Boolean, $project: [Int]) {\n  adverts: advertList(ids: $ids, developer: $developer, project: $project, offerType: $offerType, estateType: $estateType, disposition: $disposition, ownership: $ownership, construction: $construction, equipped: $equipped, priceFrom: $priceFrom, priceTo: $priceTo, surfaceFrom: $surfaceFrom, surfaceTo: $surfaceTo, limit: $limit, offset: $offset, order: $order, boundary: $boundary) {\n    totalCount\n    list {\n      id\n      uri\n      type\n      advertType\n      offerType\n      address\n      shortDescription(breakLine: false, offerEstateType: true, disposition: true, surface: true)\n      images(limit: 5) {\n        id\n        url(filter: RECORD_THUMB_NEWS)\n        __typename\n      }\n      active\n      reserved\n      hasTour360\n      badge {\n        text\n        class\n        __typename\n      }\n      timeExpiration\n      visitCount\n      positionCounty\n      positionCity\n      extensionAction\n      hash\n      priceFormatted\n      mainImageUrl(filter: RECORD_MAIN_NOWM)\n      advertUserstate(state: FAVOURITE) {\n        id\n        state\n        __typename\n      }\n      user {\n        id\n        __typename\n      }\n      advertObject {\n        id\n        address\n        estateType\n        offerType\n        ... on AdvertEstateOffer {\n          price\n          disposition\n          surface\n          dataJson\n          __typename\n        }\n        __typename\n      }\n      tags(locale: $locale)\n      lastUserVisit {\n        id\n        date\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
            "variables": {
                "ids": ids,
                "locale": "cs"
            },
            "operationName": "Adverts",
        }

        return scrapy.http.JsonRequest(url="https://www.bezrealitky.cz/webgraphql", data=data, callback=self.parse_graphql)

class JsonWriterPipeline(object):
    items = {}

    def open_spider(self, spider):
        try:
            with open("bezrealitky.json","r") as f:
                self.items = json.load(f)
        except FileNotFoundError as _:
            pass

    def close_spider(self, spider):
        with open("bezrealitky.json","w+") as f:
            json.dump(self.items, f, sort_keys=True, indent=4, separators=(',', ': '))

    def process_item(self, item, spider):
        if item["link"] not in self.items:
            item["time"] = time.time()
            self.items[item["link"]] = item
