#-*- coding: utf8 -*-

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy import log
import re
from kinopoisk.items import KinopoiskItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


reImageUrl = re.compile(r"http://st.kinopoisk.ru/images/film/\d+.jpg", re.DOTALL)
reFrameUrl = re.compile(r'"previewFile": "(.*?)"')
reRusName = re.compile(r'"moviename-big" itemprop="name">(.*?)<')
reEngName = re.compile(r'itemprop="alternativeHeadline">(.*?)<')
reDirector = re.compile(r'itemprop="director"><.*?>(.*?)<')
reAge = re.compile(r'class="ageLimit age(\d+)"')
reMpaa = re.compile(r'class="rate_(.*?)"')
reActorSearch = re.compile('class="actor_list".*?<div(.*?)</div', re.DOTALL)
reActorFindall = re.compile(r'itemprop="name">(.*?)</a')
reId = re.compile(r'/(\d+).*$')

reFilmId = re.compile(r'<div class="name"><a href="/level/1(/film/\d+)')


class KinoSpider(BaseSpider):
	name = 'KinoSpider'
	
	def start_requests(self):
		for x in range(0, 187):
			yield Request('http://www.kinopoisk.ru/top/navigator/order/rating/page/%d/#results' % x, callback=self.parse_FULLpage)

	def parse_FULLpage(self, response):
		FilmFromPage = reFilmId.findall(response.body)			
		for film in  FilmFromPage:
			yield Request('http://www.kinopoisk.ru' + film, callback=self.parse_page)

	def parse_page(self, response):
		print(response.url)
		body = response.body.decode('cp1251')
		item = KinopoiskItem()
		item['image_urls'] = image_urls = []
		try:
			 image_urls.append(reImageUrl.search(body).group())
		except AttributeError:
			pass
			
		try:
			image_urls.append("http://tr.kinopoisk.ru/"+reFrameUrl.search(body).group(1))
		except AttributeError:
			pass

		item['RusName'] = reRusName.search(body).group(1)	
		try:
			item['EngName'] = reEngName.search(body).group(1)
		except AttributeError:
			item['EngName'] = ''

		item['Director'] = reDirector.search(body).group(1)
		
		try:
			item['Age'] = reAge.search(body).group(1)
		except AttributeError:
			item['Age'] = ''

		try:
			item['RateMpaa'] = reMpaa.search(body).group(1)
		except AttributeError:
			item['RateMpaa'] = ''

		try:
			stroka = reActorSearch.search(body).group(1)
			item['ActorsList'] = reActorFindall.findall(stroka)[:-1]
		except AttributeError:
			item['ActorsList'] = []


		item['Id'] = reId.search(response.url).group(1)
		return item
