from scrapy import log
from scrapy import signals
from scrapy.exceptions import NotConfigured, DropItem
import MySQLdb

class MySQLExporter(object):
	def __init__(self, mysqlConnection):
		self.connection = mysqlConnection
		self.cursor = mysqlConnection.cursor()
		log.msg(message="MySQLExporter - initiate", _level = log.INFO)


	@classmethod
	def from_crawler(cls, crawler):
		user = crawler.settings.get('MySQLUser', 'root')
		passwd = crawler.settings.get('MySQLPassw', 'kate')
		host = crawler.settings.get('MySQLHost', 'localhost')
		db = crawler.settings.get('MySQLdb', 'kino')
		mysqlConnection = MySQLdb.connect(host = host, user= user, passwd = passwd, db=db)
		cls = cls(mysqlConnection)
		crawler.signals.connect(cls.item_scraped, signal=signals.item_scraped)
		
		return cls

	def item_scraped(self, item, spider):
		try:
			log.msg(message = "MySQLExporter, item_scraped incercam sa scriem", _level = log.INFO)
			self.cursor.execute('INSERT INTO main (ID, EngName, RusName, Director, Mpaa) VALUES (%s, %s, %s, %s, %s)', (item['Id'], item['EngName'], item['RusName'], item['Director'], item['RateMpaa']))
			self.cursor.executemany('INSERT INTO actors (ID, AName) VALUES(%s, %s)', [(item['Id'], x) for x in item['ActorsList']])
			try:
				item['images'][1]
			except:
				pass
			else:
				subst = 'frame'
				if 'image' in item['images'][1]['url']: subst='image'

				frame_file = open('MyImage/'+item['images'][1]['path'], 'rb')
				self.cursor.execute('INSERT INTO image (ID, TypeOf, Content) VALUES(%s, %s, %s)', (item['Id'], subst, MySQLdb.escape_string(frame_file.read())))	
				frame_file.close()
			
			
			try:
				item['images'][0]
			except:
				pass
			else:
				subst = 'frame'
				if 'image' in item['images'][0]['url']: subst='image'
				image_file = open('MyImage/'+item['images'][0]['path'], 'rb')
				self.cursor.execute('INSERT INTO image (ID, TypeOf, Content) VALUES(%s, %s, %s)', (item['Id'], subst, MySQLdb.escape_string(image_file.read())))	
				image_file.close()
		except Exception as e:

			print(e)
			return DropItem

		else:
			self.connection.commit()
			return item
