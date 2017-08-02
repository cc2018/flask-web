# -*- coding: utf-8 -*-

import os
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

# db data
client = MongoClient('mongodb://localhost:27017/')
db = client.cms
collection = db.articles

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.route('/')
def show_articles():
    data = collection.find({'article_type': 1}).sort([('create_at',-1)]);
    return 'hddd'
    #return render_template('index.html', jokes=data)


if __name__ == '__main__':
    app.run()
