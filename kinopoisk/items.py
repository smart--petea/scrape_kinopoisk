# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class KinopoiskItem(Item):
	RusName = Field()
	EngName = Field()
	Director = Field()
	ActorsList = Field()
	image_urls = Field()
	images = Field()
	Age = Field()
	RateMpaa = Field()
	Id = Field()
	
