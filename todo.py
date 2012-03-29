#!/usr/bin/env python
#all the imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, render_template


#configuration
DATABASE = 'todo.db'
DEBUG = True
SECRET_KEY = 'development key'


#our little application
app = Flask(__name__)
app.config.from_envvar('TODO_SETTINGS',silent=True)


#database connection
def connect_db():
    return sqlite3.connect(DATABASE)


#initialising database
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()
    

@app.teardown_request
def teardown_request(exception):
    g.db.close()
    
    

#add template paths and rendering it
@app.route('/')
@app.route('/templates')
def view(name=None):
    return render_template('index.html',name=name)
    
    
if __name__ == '__main__':
    init_db()
    app.run()
    

