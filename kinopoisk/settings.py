# Scrapy settings for kinopoisk project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'kinopoisk'

SPIDER_MODULES = ['kinopoisk.spiders.spiderino']
NEWSPIDER_MODULE = 'kinopoisk.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'kinopoisk (+http://www.yourdomain.com)'
LOG_FILE = 'crawl.log'
ITEM_PIPELINES = ['scrapy.contrib.pipeline.images.ImagesPipeline']
IMAGES_STORE = 'MyImage'
MySQLUser = 'root'
MySQLHost = 'localhost'
MySQLdb = 'kino'
MySQLPassw = 'kate'
EXTENSIONS = {
			'kinopoisk.MySQLExporter.MySQLExporter': 500
			}
