# -*- coding: utf-8 -*-

import mysql.connector

 
class DB(object):

    def __init__(self, DB_HOST, DB_PORT, DB_USER, DB_PWD, DB_NAME):
        self.DB_HOST = DB_HOST  #设置MYSQL地址
        self.DB_PORT = DB_PORT  #设置端口号
        self.DB_USER = DB_USER  #设置用户名
        self.DB_PWD = DB_PWD    #设置密码
        self.DB_NAME = DB_NAME  #数据库名
        
        self.conn = self.get_conn()
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
    #db = DB('127.0.0.1',3306,'root','','wordpress')
    #print db.query("show tables;")