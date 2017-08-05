# -*- coding: utf-8 -*-

import os

import datetime
from pymongo import MongoClient
#from flaskext.markdown import Extension, Markdown
from flask_misaka import Misaka
from flask_misaka import markdown
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from posts import Posts

import re

#from misaka import Markdown, HtmlRenderer
#rndr = HtmlRenderer()
#md = Markdown(rndr)

app = Flask(__name__)
#md = Markdown(app, safe_mode=False)
#md.register_extension(SimpleExtension)
Misaka(app)


# db data
client = MongoClient('mongodb://localhost:27017/')
db = client.cms
articles = db.articles
org_articles = db.org_articles

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

posts = Posts(app.root_path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/article')
def show_articles():
    articles = []
    for item in posts:
        articles.append(posts[item])

    return render_template('article.html', articles=articles)


@app.route('/article/<int:year>/<int:month>/<int:day>/<title>')
def show_post(year, month, day, title):
    file_info = posts['%d-%02d-%d-%s.md' % (year, month, day, title)]
    if file_info is not None:
        with app.open_resource(file_info['path']) as f:
            content = f.read().decode('utf-8')
            body_pattern = re.compile('---[\w\W]*?---([\w\W]*)')
            rv = re.search(body_pattern, content)
            body = rv.group(1)

            data = {
                'content': markdown(body, fenced_code=True)
            }
            return render_template('post.html', post=data)

    return redirect(url_for('show_index'))


@app.route('/')
def show_index():
    data = articles.find({'article_type': 1}).sort([('create_at',-1)]);
    return render_template('index.html', jokes=data)


if __name__ == '__main__':
    app.run()
