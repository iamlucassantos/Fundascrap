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

        # Amsterdam links
        ams_buurt_str = """jordaan,kadoelen,kinkerbuurt,landlust,lutkemeer-ookmeer,middelveldsche-akerpolder,middenmeer,ijburg-oost,ijburg-west,ijburg-zuid,ijplein-vogelbuurt,ijselbuurt,indische-buurt-oost,indische-buurt-west,grachtengordel-west,grachtengordel-zuid,haarlemmerbuurt,helmersbuurt,holendrecht-reigersbos,hoofddorppleinbuurt,hoofdweg-eo,houthavens,de-punt,de-weteringschans,driemond,eendracht,elzenhagen,erasmuspark,frankendael,frederik-hendrikbuurt,gein,geuzenbuurt,geuzenveld,buikslotermeer,buitenveldert-oost,buitenveldert-west,burgwallen-nieuwe-zijde,burgwallen-oude-zijde,centrale-markt,chassebuurt,da-costabuurt,dapperbuurt,de-kolenkit,apollobuurt,banne-buiksloot,bedrijventerrein-sloterdijk,betondorp,bijlmer-centrum-dfh,bijlmer-oost-egk,museumkwartier,nellestein,nieuwe-pijp,nieuwendammerdijk-buiksloterdijk,nieuwmarkt-lastage,noordelijke-ij-oevers-oost,noordelijke-ij-oevers-west,omval-overamstel,oostelijk-havengebied,oostelijke-eilanden-kadijken,oosterparkbuurt,oostzanerwerf,osdorp-midden,osdorp-oost,oude-pijp,overtoomse-sluis,overtoomse-veld,prinses-irenebuurt-eo,rijnbuurt,scheldebuurt,schinkelbuurt,sloter-riekerpolder,sloterdijk,slotermeer-noordoost,slotermeer-zuidwest,slotervaart-noord,slotervaart-zuid,spaarndammer-en-zeeheldenbuurt,staatsliedenbuurt,stadionbuurt,transvaalbuurt,tuindorp-buiksloot,tuindorp-nieuwendam,tuindorp-oostzaan,van-galenbuurt,van-lennepbuurt,volewijck,vondelbuurt,water,waterland,waterlandpleinbuurt,weesperbuurt-plantage,weesperzijde,westindische-buurt,westlandgracht,willemspark,westelijk-havengebied,zeeburgereiland-nieuwe-diep,zuid-pijp,zuidas"""
        ams_buurt = set(ams_buurt_str.split(','))
        ams_url = [f'https://www.funda.nl/koop/amsterdam/{buurt}/{min_price}-{max_price}/' for buurt in ams_buurt]

        # Utrecht links
        utr_buurt_str = """2e-daalsebuurt-en-omgeving,abstede-tolsteegsingel-eo,bedrijventerrein-lageweide,bleekstraat-en-omgeving,bokkenbuurt,breedstraat-en-plompetorengracht-en-omgeving,breedstraat-en-plompetorengracht-en-omgeving,buiten-wittevrouwen,dichterswijk,domplein-neude-janskerkhof,egelantierstraat-mariendaalstraat-eo,elinkwijk-en-omgeving,galgenwaard-en-omgeving,geuzenwijk,grauwaart,halve-maan-noord,halve-maan-zuid,het-zand-oost,het-zand-west,hoge-weide,hooch-boulandt,hoog-catharijne-ns-en-jaarbeurs,huizingalaan-k-doormanlaan-en-omgeving,julianapark-en-omgeving,kanaleneiland-noord,kanaleneiland-zuid,l-napoleonplantsoen-en-omgeving,laan-van-nieuw-guinea-spinozaweg-eo,lange-elisabethstraat-mariaplaats-en-omgeving,lange-nieuwstraat-en-omgeving,langerak,lauwerecht,leeuwesteyn,leidsche-rijn-centrum,leidseweg-en-omgeving,lombok-oost,lombok-west,lunetten-noord,lunetten-zuid,maarschalkerweerd-en-mereveld,neckardreef-en-omgeving,nieuw-engeland-th-a-kempisplantsoen-en-omgeving,nieuw-hoograven-noord,nieuw-hoograven-zuid,nieuwegracht-oost,nijenoord-hoogstraat-en-omgeving,nobelstraat-en-omgeving,ondiep,oog-in-al,oud-hoograven-noord,oud-hoograven-zuid,oudwijk,parkwijk-noord,parkwijk-zuid,pijlsweerd-noord,pijlsweerd-zuid,poldergebied-overvecht,prins-bernhardplein-en-omgeving,queeckhovenplein-en-omgeving,rijnenburg,rijnsweerd,rijnvliet,rivierenwijk,rubenslaan-en-omgeving,schaakbuurt-en-omgeving,schepenbuurt-cartesiusweg-eo,schildersbuurt,springweg-en-omgeving-geertebuurt,staatsliedenbuurt,taag-en-rubicondreef-en-omgeving,terwijde-oost,terwijde-west,tigrisdreef-en-omgeving,tolsteeg-en-rotsoord,transwijk-noord,transwijk-zuid,tuindorp-en-van-lieflandlaan-west,tuindorp-oost,tuinwijk-oost,tuinwijk-west,vechtzoom-noord-klopvaart,vechtzoom-zuid,vogelenbuurt,voordorp-en-voorveldsepolder,watervogelbuurt,welgelegen-den-hommel,wijk-c,wilhelminapark-en-omgeving,wittevrouwen,wolga-en-donaudreef-en-omgeving,zambesidreef-en-omgeving,zamenhofdreef-en-omgeving,zeeheldenbuurt-hengeveldstraat-en-omgeving,zuilen-noord"""
        utr_buurt = set(utr_buurt_str.split(','))
        utr_url = [f'https://www.funda.nl/koop/utrecht/{buurt}/{min_price}-{max_price}/' for buurt in utr_buurt]

        # Rotterdam links
        rot_buurt_str = """afrikaanderwijk,agniesebuurt,bergpolder,beverwaard,blijdorp,bloemhof,bospolder,carnisse,charlois-zuidrand,cool,cs-kwartier,de-esch,delfshaven,dijkzigt,feijenoord,groot-ijsselmonde,heijplaat,het-lage-land,hillegersberg-noord,hillegersberg-zuid,hillesluis,katendrecht,kleinpolder,kop-van-zuid,kop-van-zuid-entrepot,kralingen-oost,kralingen-west,kralingse-bos,kralingseveer,liskwartier,lombardijen,middelland,molenlaankwartier,nesselande,nieuw-crooswijk,nieuwe-werk,nieuwe-westen,noordereiland,ommoord,oosterflank,oud-charlois,oud-crooswijk,oud-ijsselmonde,oud-mathenesse,oude-noorden,oude-westen,overschie,pendrecht,prinsenland,provenierswijk,rubroek,schiebroek,schiemond,schieveen,s-gravenland,spangen,stadsdriehoek,struisenburg,tarwewijk,terbregge,tussendijken,vreewijk,zestienhoven,zevenkamp,zuiderpark,zuidplein,zuidwijk"""
        rot_buurt = set(rot_buurt_str.split(','))
        rot_url = [f'https://www.funda.nl/koop/rotterdam/{buurt}/{min_price}-{max_price}/' for buurt in rot_buurt]

        self.start_urls = ams_url + utr_url + rot_url

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
