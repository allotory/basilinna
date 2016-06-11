# -*- coding: utf-8 -*-

import mysql.connector
import configparser

 
class DB(object):

    def __init__(self, database):
        
        #读取配置文件
        config = configparser.ConfigParser()
        config.read("config.cfg")

        self.DB_HOST = config.get(database, "host")  #设置MYSQL地址
        self.DB_PORT = config.get(database, "port")  #设置端口号
        self.DB_USER = config.get(database, "user")  #设置用户名
        self.DB_PWD = config.get(database, "password")    #设置密码
        self.DB_NAME = config.get(database, "database")  #数据库名
        
        self.conn = self.get_conn()
        # self.conn.autocommit(True)
        self.cursor = self.conn.cursor()
 
    def get_conn(self):
        return mysql.connector.Connect(
            host = self.DB_HOST,  
            port = self.DB_PORT,  
            user = self.DB_USER,  
            passwd = self.DB_PWD, 
            db = self.DB_NAME,
            #设置编码 
            charset = 'utf8'
           )
 
    def query(self, sql):
        count = self.cursor.execute(sql)
        result_set = self.cursor.fetchall()
        return result_set

    def insert(self, sql):
        count = self.cursor.execute(sql)
        self.conn.commit()
        return count
    
    def update(self, sql):
        count = self.cursor.execute(sql)
        self.conn.commit()
        return count

    def delete(self, sql):
        count = self.cursor.execute(sql)
        self.conn.commit()
        return count

    def close(self):
        self.cursor.close()
        self.conn.close()
 
if __name__ == "__main__":
    db = DB('mysql')
    print(db.DB_NAME)