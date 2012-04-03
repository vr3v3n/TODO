#!/usr/bin/env python
#all the imports
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from contextlib import closing
from flask import Flask, render_template, g, jsonify, request, json
import conf
import json




#our little application
app = Flask(__name__)
app.config.from_object(conf)
app.config.from_envvar('TODO_SETTINGS',silent=True)


#database connection
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


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
    


@app.route('/showList' , methods=['POST'])
def show_list():
    if request.method == 'POST':
        cur = g.db.execute('select * from entries order by id desc')
    #entryDict = {}
    
        entries = [dict(title=row[1]) for row in cur.fetchall()]
        print entries
        #return jsonify(entries)
        return json.dumps(entries)
    else:
        return '0'
    
@app.route('/addList', methods = ['POST'])
def add_entry():
    if request.method == 'POST':
        g.db.execute('insert into entries(title) values(?)',
                    [request.form['list']])
        g.db.commit()
        return '1'
    return '0'


#add template paths and rendering it
@app.route('/')
def view():
    return render_template('index.html')
    
    
if __name__ == '__main__':
    init_db()
    app.run()
    

