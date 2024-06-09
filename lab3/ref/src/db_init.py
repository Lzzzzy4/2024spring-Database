# -*- coding: utf-8 -*-
"""
@Time    : 2021/6/29 14:20
@Author  : 和泳毅
@FileName: db_init.py
@SoftWare: PyCharm
"""

from flask_sqlalchemy import SQLAlchemy
import mysql.connector
# from sqlalchemy import create_engine



db2 = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='bank'
)

# username = 'root'
# password = '123456'
# host = '127.0.0.1'
# port = '3306'
# database = 'bank'
# engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

db = SQLAlchemy()