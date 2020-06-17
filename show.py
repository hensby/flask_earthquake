import sqlite3
from flask.templating import render_template
from pyecharts import Scatter,configure
from flask import Flask

conn=sqlite3.connect('test.db')
print("Open database successfully")
c=conn.cursor()
c.execute("select * from all_month")
data = c.fetchall()
conn.close()

app = Flask(__name__)


@app.route('/dist',methods=['GET'])
def tmp():
    es = Scatter()
    x = []
    y = []
    for item in data:
        x.append(item[2])
        y.append(item[3])
    es.add('', x, y)
    es.render('1.html')
    return render_template('1.html')

