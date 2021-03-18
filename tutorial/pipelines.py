# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import MySQLdb

class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host):
        self.db = db
        self.user = user
        self.passwd = passwd
        self.host = host


    @classmethod
    def from_crawler(cls,crawler):
        db_settings     = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db              = db_settings['db']
        user            = db_settings['user']
        host            = db_settings['host']
        passwd = db_settings['passwd']
        return cls(db,user,passwd,host)

    def open_spider(self,spider):
        self.conn       = MySQLdb.connect(db = self.db,user=self.user,
                                            password=self.passwd,host=self.host)
        self.cursor     = self.conn.cursor()

    def process_item(self, item, spider):
        sql             = "INSERT INTO Items(Item) VALUES('%s')"%(str(item.get('title')))
        print(sql)
        # print("item",Item)
        # print(item)
        # print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.close()
