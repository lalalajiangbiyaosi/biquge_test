# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from biquge.items import BiqugeItem,Book_content_Item
import pymysql,os
class BiqugePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item,BiqugeItem):
            try:
                db = pymysql.connect("39.106.36.143","root","root","biquge_book",use_unicode=True, charset="utf8")
                cursor = db.cursor()
                cursor.execute('insert into book_index(name,author,brief,update_chapter) values(%s, %s, %s, %s)' , (item['name'],item['author'],item['brief'],item['update_chapter']))
            except Exception as e:
                print("输出数据库错误！",e)
                with open('./err_book_index.txt', 'a', encoding='utf-8') as f:
                    f.write(item['id_name'] + '  ' + item['name'] + '  \n')
            finally:

                db.commit()
                db.close()
            # with open(item['name']+'.txt','w',encoding='utf-8') as f :
            #     f.write(item['author'])
            #     f.write(item['brief'])
        elif isinstance(item,Book_content_Item):
            try:
                db = pymysql.connect("39.106.36.143", "root", "root", "biquge_book", use_unicode=True, charset="utf8")

                cursor = db.cursor()
                cursor.execute('insert into book_chapter_content(book_name,chapter_name,chapter_id) values(%s, %s, %s)' , (item['book_name'],item['chapter_name'],int(item['chapter_id'])))
                db.commit()
                db.close()
            except Exception as e:
                print("连接数据库失败",e)
                with open('./err_book_chapter.txt', 'a', encoding='utf-8') as f:
                    f.write(item['book_name'] + '  ' + item['chapter_name'] + '  \n')
            try:
                if not os.path.exists(item['book_name']):
                    os.mkdir(item['book_name'])
                with open('./'+item['book_name']+'/'+item['chapter_name']+'.txt','w',encoding='utf-8') as f:
                    f.write(item['content'])
            except Exception as e:
                print(e)
            return item

