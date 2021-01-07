from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd242b6b60ac4bdb0d635b8ddfa050a4c'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'ShoeUse'

mysql = MySQL(app)

from shoeuse import routes