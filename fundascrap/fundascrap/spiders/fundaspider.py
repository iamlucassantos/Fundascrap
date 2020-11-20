"""
Created on 19/11/2020

@author: Lucas V. dos Santos
"""

import scrapy
from fundascrap.items import FundascrapItem
import re


class FundaSpider(scrapy.Spider):
    name = "funda"

    def __init__(self):
        min_price = 400000
        max_price = 900000
        ams_buurt_str = """jordaan,kadoelen,kinkerbuurt,landlust,lutkemeer-ookmeer,middelveldsche-akerpolder,middenmeer,ijburg-oost,ijburg-west,ijburg-zuid,ijplein-vogelbuurt,ijselbuurt,indische-buurt-oost,indische-buurt-west,grachtengordel-west,grachtengordel-zuid,haarlemmerbuurt,helmersbuurt,holendrecht-reigersbos,hoofddorppleinbuurt,hoofdweg-eo,houthavens,de-punt,de-weteringschans,driemond,eendracht,elzenhagen,erasmuspark,frankendael,frederik-hendrikbuurt,gein,geuzenbuurt,geuzenveld,buikslotermeer,buitenveldert-oost,buitenveldert-west,burgwallen-nieuwe-zijde,burgwallen-oude-zijde,centrale-markt,chassebuurt,da-costabuurt,dapperbuurt,de-kolenkit,apollobuurt,banne-buiksloot,bedrijventerrein-sloterdijk,betondorp,bijlmer-centrum-dfh,bijlmer-oost-egk,museumkwartier,nellestein,nieuwe-pijp,nieuwendammerdijk-buiksloterdijk,nieuwmarkt-lastage,noordelijke-ij-oevers-oost,noordelijke-ij-oevers-west,omval-overamstel,oostelijk-havengebied,oostelijke-eilanden-kadijken,oosterparkbuurt,oostzanerwerf,osdorp-midden,osdorp-oost,oude-pijp,overtoomse-sluis,overtoomse-veld,prinses-irenebuurt-eo,rijnbuurt,scheldebuurt,schinkelbuurt,sloter-riekerpolder,sloterdijk,slotermeer-noordoost,slotermeer-zuidwest,slotervaart-noord,slotervaart-zuid,spaarndammer-en-zeeheldenbuurt,staatsliedenbuurt,stadionbuurt,transvaalbuurt,tuindorp-buiksloot,tuindorp-nieuwendam,tuindorp-oostzaan,van-galenbuurt,van-lennepbuurt,volewijck,vondelbuurt,water,waterland,waterlandpleinbuurt,weesperbuurt-plantage,weesperzijde,westindische-buurt,westlandgracht,willemspark,westelijk-havengebied,zeeburgereiland-nieuwe-diep,zuid-pijp,zuidas"""
        ams_buurt = set(ams_buurt_str.split(','))
        ams_url = [f'https://www.funda.nl/koop/amsterdam/{buurt}/{min_price}-{max_price}/' for buurt in ams_buurt]

        self.start_urls = ams_url

    def parse(self, response):
        for post in response.css('div.search-result-content-inner'):
            item = FundascrapItem()
            city = re.search('koop/(.*?)/', response.url)
            buurt = re.search('koop/.*?/(.*?)/', response.url)

            item['city'] = city.group(1) if city else ''
            item['buurt'] = buurt.group(1) if buurt else ''
            item['link'] = 'https://www.funda.nl/' + post.css(
                'div.search-result__header-title-col a::attr(href)').get().strip()
            item['title'] = post.css('h2.search-result__header-title::text').get().strip()
            item['subtitle'] = post.css('h4.search-result__header-subtitle::text').get().strip()
            item['price'] = post.css('span.search-result-price::text').get().strip().split()[1].replace('.','')
            try:
                item['area1'] = re.search('(\d+)', post.css('ul.search-result-kenmerken li span::text')[0].get()).group(
                    1)
            except IndexError:
                item['area1'] = ''
            try:
                item['area2'] = re.search('(\d+)', post.css('ul.search-result-kenmerken li span::text')[1].get()).group(
                    1)
            except IndexError:
                item['area2'] = ''
            try:
                item['rooms'] = re.search('(\d+)', post.css('ul.search-result-kenmerken li')[1].get()).group(1)
            except IndexError:
                item['rooms'] = ''
            yield item

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


def main():
    pass


if __name__ == "__main__":
    main()
# response.css('title::text').get()
# response.css('title::text').getall()
# search-result-content-inner
# >scrapy crawl funda -o posts.json
