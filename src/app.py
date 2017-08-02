# -*- coding: utf-8 -*-

import os
import datetime
from pymongo import MongoClient
from flaskext.markdown import Markdown
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

#from misaka import Markdown, HtmlRenderer
#rndr = HtmlRenderer()
#md = Markdown(rndr)

app = Flask(__name__)
md = Markdown(app, safe_mode=False)
#md = Markdown(app,
#    extensions=['footnotes'],
#    extension_configs={'footnotes': ('PLACE_MARKER','~~~~~~~~')},
#    safe_mode=True,
#    output_format='html4',
#)

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

@app.route('/edit', methods=['GET', 'POST'])
def edit_articles():
    if 'logged_in' in session and session['logged_in'] == True:
        if request.method == 'POST':
            title = request.form['write-title']
            desc = request.form['write-desc']
            tags = request.form['write-tags']
            content = md(request.form['write-body'])
            post = {
                'article_type': 2,
                'id': 2,
                'author': 'Sombody Cao',
                'title': title,
                'desc': desc,
                'tags': tags,
                'content': content,
                'create_at': datetime.datetime.utcnow(),
                'update_at': datetime.datetime.utcnow()
            }
            org_articles.insert_one(post)
            return redirect(url_for('show_index'))
        return render_template('edit.html')

    else:
        return redirect(url_for('login'))

@app.route('/articles')
def show_articles():
    data = org_articles.find().sort([('create_at',-1)]);
    return render_template('articles.html', articles=data)

@app.route('/')
def show_index():
    data = articles.find({'article_type': 1}).sort([('create_at',-1)]);
    return render_template('index.html', jokes=data)


if __name__ == '__main__':
    app.run()
