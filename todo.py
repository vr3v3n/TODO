# TODO.py
# Copyright (C) 2012 Varun Rana<varunrana.in>
# Developer :Varun Rana
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>
#

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
    

#show all TODO items 
@app.route('/showList' , methods=['POST'])
def show_list():
    if request.method == 'POST':
        cur = g.db.execute('select * from entries order by id desc')
        entries = [dict(title=row[1],done=row[2]) for row in cur.fetchall()]
        return json.dumps(entries)
    else:
        return '0'

#Add items to the database or list
@app.route('/addList', methods = ['POST'])
def add_entry():
    if request.method == 'POST':
        g.db.execute('insert into entries(title) values(?)',
            [request.form['list']]
        )
        g.db.commit()
        return '1'
    return '0'


#marked item as done
@app.route('/altList', methods=['POST'])
def alt_List():
    if request.method == 'POST':
        g.db.execute('update entries SET done="1" WHERE title="'+request.form['title']+'"')
        g.db.commit()
        return '1'
    return '0'


#undo the marked item
@app.route('/undoList', methods=['POST'])
def undo_List():
    if request.method == 'POST':
        g.db.execute('update entries SET done="0" WHERE title="'+request.form['title']+'"')
        g.db.commit()
        return '1'
    return '0'


#delete completed items from the list or database
@app.route('/deleteList', methods=['POST'])
def del_List():
    if request.method == 'POST':
        g.db.execute('DELETE FROM entries WHERE done="1"')
        g.db.commit()        
        return '1'
    return '0'

#add template paths and rendering it
@app.route('/')
def view():
    return render_template('index.html')
    
    
if __name__ == '__main__':
    
#calling init_db() to create database on client side
    init_db() 

#Calling app.run() to start the app
    app.run()
    

