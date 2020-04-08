# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from bokeyuan.settings import host, user, password
from bokeyuan.settings import db_name, table_name


class BokeyuanPipeline(object):
    def __init__(self):
        self.db = pymysql.connect(host=host, user=user, password=password, port=3306, charset='utf8mb4')  # 创建连接
        self.cursor = self.db.cursor()  # 获取光标
        print('数据库连接成功 。。。')

        self.create_db()  # 创建数据库

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            print('数据库关闭成功')

    def process_item(self, item, spider):
        print('抓取数据 : ', list(item.items()))
        self.save_item_to_db(item)  # 保存数据至数据库
        return item

    def create_db(self):
        """ 创建数据库和数据表 """
        # 创建数据库
        try:
            if not self.cursor.execute("select * from information_schema.SCHEMATA where SCHEMA_NAME='%s';" % db_name):
                print('数据库 %s 虽然还不存在，但是数据库正在创建' % db_name)
                self.cursor.execute("create database %s character set utf8mb4;" % db_name)
                print('数据库 %s 虽然还不存在，但是已经创建成功' % db_name)
            else:
                print('数据库 %s 其实已经存在' % db_name)
        finally:
            try:
                self.cursor.execute('use %s;' % db_name)
                print('数据库切换到 %s 操作' % db_name)
            except Exception as e:
                print('databases create error :', e.args)

        # 创建数据表
        if not self.cursor.execute(
                "select table_name from information_schema.TABLES where table_name='%s';" % table_name):
            try:
                print('数据表 %s 虽然还不存在，但是正在创建' % table_name)
                create_table_sql = """
                CREATE TABLE {table_name}(
                    # `id` int(12) AUTO_INCREMENT COMMENT 'id',  # 设置id自增
                    `author` varchar(50) COMMENT '作者',
                    `issue_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
                    `num_comment` int(10) NULL DEFAULT NULL COMMENT '评论数',
                    `num_read` int(10) NULL DEFAULT NULL COMMENT '阅读数',
                    `title` varchar(480) NOT NULL COMMENT '标题',
                    `num_recommend` int(10) NULL DEFAULT NULL COMMENT '推荐数',
                    PRIMARY KEY (`author`) USING BTREE
                    ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci  ROW_FORMAT = Compact;
                    """.format(table_name=table_name)
                # self.cursor.execute("create table %s(id int,name char(20))character set utf8mb4;" % table_name)
                self.cursor.execute(create_table_sql)
                print('数据表 %s 虽然还不存在，但是已经创建成功' % table_name)
            except Exception as e:
                print('table create error :', e.args)
        else:
            print('数据表 %s 已存在' % table_name)

    def save_item_to_db(self, item):
        """ 保存 item 至数据库 """
        # print('采集到数据 :', item)
        describe = ['author', 'issue_time', 'num_comment', 'num_read', 'title', 'num_recommend']
        keys = ', '.join(describe)
        values = ', '.join(['%s'] * len(describe))
        items = [item.get(key) for key in describe]
        # print(list(zip(keys, values)))
        try:
            # update_sql = """INSERT INTO {table} ({keys}) VALUES ({values})""".format(table=table, keys=keys, values=values)
            update_sql = 'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(
                table=table_name, keys=keys, values=values)
            update = ','.join([' {key} = %s'.format(key=key) for key in describe])
            update_sql += update
            if self.cursor.execute(update_sql, items * 2):
                # print('update list to database ......', item)
                self.db.commit()
            # else:
            #     print('数据已存在', items)
        except Exception as e:
            print('Error Reason:', str(e.args).encode().decode('unicode-escape'))
            self.db.rollback()
