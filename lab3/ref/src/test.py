import sys
sys.path.append("C:\\users\lenovo\\appdata\\local\\programs\\python\\python310\\lib\\site-packages")
from flask import Flask, render_template, request, abort
import config
import numpy as np
import datetime
from db_init import db, db2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import Bank, Client, Employee, SavingAccount, CheckingAccount, Loan, Apply, \
    Account, Contact, Department, Own, Service, Checking, User
import time

from flask_sqlalchemy import SQLAlchemy
import mysql.connector

db = SQLAlchemy()

db2 = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    passwd='123456',
    database='bank'
)


newUser = User(
    username="123",
    userkey="123",
    )
# print(newUser)

db.session.add(newUser)