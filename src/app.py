# -*- coding: utf-8 -*-

import os

import datetime
from pymongo import MongoClient
from flaskext.markdown import Markdown
#from flask.ext.misaka import Misaka
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from posts import Posts

#from misaka import Markdown, HtmlRenderer
#rndr = HtmlRenderer()
#md = Markdown(rndr)

app = Flask(__name__)
md = Markdown(app, safe_mode=False)
#Misaka(app)

# db data
client = MongoClient('mongodb://172.18.182.4:27017/')
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


@app.route('/article')
def show_articles():
    # data = org_articles.find().sort([('create_at',-1)]);
    return render_template('article.html', articles=posts)


@app.route('/article/<int:year>/<int:month>/<int:day>/<title>')
def show_post(year, month, day, title):
    file_info = posts['%d-%02d-%d-%s.md' % (year, month, day, title)]
    if file_info is not None:
        with app.open_resource(file_info['path']) as f:
            content = f.read()
            data = {
                'content': content.decode('utf-8')
            }
            return render_template('post.html', post=data)

    return redirect(url_for('show_index'))


@app.route('/')
def show_index():
    data = articles.find({'article_type': 1}).sort([('create_at',-1)]);
    return render_template('index.html', jokes=data)


if __name__ == '__main__':
    app.run()
