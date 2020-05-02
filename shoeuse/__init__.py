from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'd242b6b60ac4bdb0d635b8ddfa050a4c'


from shoeuse import routes