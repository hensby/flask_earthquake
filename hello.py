import os
from flask import Flask, request
from flask.templating import render_template
import sqlite3
import math
from math import sin, asin, cos, radians, fabs, sqrt
# import datetime
from datetime import datetime, timedelta
import time
import requests

app = Flask(__name__)
port = int(os.getenv("PORT", 5000))

data = []


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    # data = getData("select * from all_month")
    if request.method == 'POST':
        if request.form['type'] == 'top':
            # data = getData("select * from all_month")
            topK = request.form['topK']
            print(topK)
            if topK == '' or topK is None:
                data = getData("select * from all_month")
                return render_template('home.html', result=data, k=len(data))
            else:
                data = getData("select * from all_month order by mag DESC limit " + topK)
                # print(data)
                return render_template('home.html', result=data, k=len(data))
        elif request.form['type'] == 'distance':
            data = []
            distance = request.form['distance']
            city = request.form['city']
            if distance == '' or city == '':
                data = getData("select * from all_month")
                return render_template('home.html', result=data, k=len(data))
            else:
                distance = int(request.form['distance'])
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                if city == "Arlington":
                    c.execute("select id from distance where distance_from_Arlington <= ?", (distance,))
                elif city == "Dallas":
                    c.execute("select id from distance where distance_from_Dallas <= ?", (distance,))
                elif city == "Anchorage":
                    c.execute("select id from distance where distance_from_Anchorage <= ?", (distance,))
                idList = c.fetchall()
                for id in idList:
                    c.execute("select * from all_month where id = ?", (id))
                    data.append(c.fetchall()[0])
                conn.close()
                return render_template('home.html', result=data, k=len(data))
            #  32.702350 + 97.122281
        elif request.form['type'] == 'searchByDateAndLevel':
            data = getData("select * from all_month")
            part = []
            start = request.form["start"]
            end = request.form["end"]
            startDate = request.form["startdate"]
            endDate = request.form["enddate"]
            print(request.form["enddate"])
            if start == '': start = 0
            if end == '': end = 100
            if startDate == '':
                startDate = datetime(1900, 6, 20)
            else:
                startDate = datetime.strptime(startDate, '%Y-%m-%d')
            if endDate == '':
                endDate = datetime(2030, 1, 1)
            else:
                endDate = datetime.strptime(endDate, '%Y-%m-%d')
            for item in data:
                if item[5] and float(start) <= float(item[5]) <= float(end) and \
                        startDate - datetime.strptime(item[1][0:10], '%Y-%m-%d') < timedelta(
                    hours=1) < endDate - datetime.strptime(item[1][0:10], '%Y-%m-%d'):
                    part.append(item)
            return render_template('home.html', result=part, k=len(part))
        elif request.form['type'] == "numbers":
            today = datetime.today()
            # today = datetime(today, '%Y-%m-%d')
            data = getData("select * from all_month")
            part1 = []
            part2 = []
            part3 = []
            partTo7 = []
            days = request.form["days"]
            for item in data:
                if item[1] and today - datetime.strptime(item[1][0:10], '%Y-%m-%d') < timedelta(days=int(days)):
                    if item[5] and float(1) <= float(item[5]) < float(2):
                        part1.append(item)
                    elif item[5] and float(2) <= float(item[5]) < float(3):
                        part2.append(item)
                    elif item[5] and float(3) <= float(item[5]) < float(4):
                        part3.append(item)
                    else:
                        partTo7.append(item)
            output = [days, len(part1), len(part2), len(part3), len(partTo7)]
            print(output)
            return render_template('home.html', result=data, k=len(data), output=output)
        elif request.form['type'] == 'common':
            distance = request.form['more_common']
            data = getData("select * from all_month")
            if distance == '':
                return render_template('home.html', result=data, k=len(data))
            else:
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute("select id from distance where distance_from_Anchorage <= ?", (distance,))
                idList1 = c.fetchall()

                conn.close()
                conn = sqlite3.connect('test.db')
                c = conn.cursor()
                c.execute("select id from distance where distance_from_Dallas <= ?", (distance,))
                idList2 = c.fetchall()

                conn.close()
            common = [distance]
            if len(idList1) > len(idList2):
                common.append("Anchorage")
                common.append("Dallas")
            else:
                common.append("Dallas")
                common.append("Anchorage")
            print(common)
            return render_template('home.html', result=data, k=len(data), common=common)

        elif request.form['type'] == 'largest_quake':
            distance = request.form["distance"]
            data = getData("select * from all_month")
            if distance == '':
                return render_template('home.html', result=data, k=len(data))
            else:
                # conn = sqlite3.connect('test.db')
                # c = conn.cursor()
                # c.execute(
                #     "select * from (select * from all_month left join distance on all_month.id = all_month.id) where distance_from_Dallas <= ? order by mag DESC limit 1",
                #     (distance,))
                # part = c.fetchall()
                # conn.close()

                city = request.form['city']
                if distance == '' or city == '':
                    data = getData("select * from all_month")
                    return render_template('home.html', result=data, k=len(data))
                else:
                    conn = sqlite3.connect('test.db')
                    print("Open database successfully")
                    c = conn.cursor()
                    if city == "Arlington":
                        c.execute("select id from distance where distance_from_Arlington <= ?", (distance,))
                    elif city == "Dallas":
                        c.execute("select id from distance where distance_from_Dallas <= ?", (distance,))
                    elif city == "Anchorage":
                        c.execute("select id from distance where distance_from_Anchorage <= ?", (distance,))
                    part = []
                    max = []
                    max_mag = 0
                    idList = c.fetchall()
                    for id in idList:
                        c.execute("select * from all_month where id = ?", (id))
                        part.append(c.fetchall()[0]);
                    for i in part:
                        if float(i[5]) > max_mag:
                            if len(max) != 0:
                                max.pop(0)
                            max.append(i)
                            max_mag = float(i[5])
                    place = [max[0][13], city, distance] # place, city, distance
            return render_template('home.html', result=max, k=len(max), place=place)



        else:
            return render_template('home.html', result=data, k=len(data))
    else:
        data = getData("select * from all_month")
        return render_template('home.html', result=data, k=len(data))


@app.route('/dist', methods=['POST'])
def dist():
    # x = []
    # y = []
    # for item in data:
    #     x.append(item[2])
    #     y.append(item[3])
    # es = Scatter()
    # es.add("Scatter", x, y)
    return render_template('1.html')


@app.route('/convert', methods=['POST'])
def convert():
    total = 0
    night = 0
    for item in data:
        if item[5] and item[5] > 4.0:
            total += 1
            a = int(math.fabs(item[3]) + 0.5)
            b = a / 15
            c = a % 15
            if (17.9 <= item[2] <= 53 and 75 <= item[3] <= 125) or (
                    40 <= item[2] <= 53 and 125 <= item[3] <= 135):
                timezone = 8
            else:
                if c > 7.5:
                    timezone = b + 1
                else:
                    timezone = b
                if item[3] > 0.0:
                    timezone = timezone
                else:
                    timezone = -timezone
            # year=int(item[1][0:4])
            # month=int(item[1][5:7])
            # day=int(item[1][8:10])
            hour = int(item[1][11:13]) + int(timezone)
            # if month==1 or month==3 or month==5 or month==7 or month==8 or month==10 or month==12:
            #     lastday=31
            #     if month==3:
            #         if year%400==0 or (year%4==0 and year%100!=0):
            #             lastlastday=29
            #         else:
            #             lastlastday=28
            #     if month==8:
            #         lastlastday=31
            # elif month==4 or month==6 or month==9 or month==11:
            #     lastday=30
            #     lastlastday=31
            # else:
            #     lastlastday=31
            #     if year%400==0 or (year%4==0 and year%100!=0):
            #         lastday=29
            #     else:
            #         lastday=28
            if hour > 24:
                hour -= 24
                # day+=1
            if 21 <= hour <= 24 or hour <= 5:
                night += 1
    return render_template('res.html', total=total, night=night)


@app.route('/scale', methods=['GET', 'POST'])
def scale():
    ip = requests.get('https://checkip.amazonaws.com').text.strip()
    print(ip)
    return render_template('res.html', ip = ip)



def getData(sql):
    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute(sql)
    # "select * from all_month"
    data = c.fetchall()
    conn.close()
    return data


EARTH_RADIUS = 6371  # Earth average radius，6371km


def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat1, lng1, city):
    lat0 = 0
    lng0 = 0
    if city == 'arlington' or city == 'Arlington':
        lat0 = radians(32.702350)
        lng0 = radians(-97.122281)
    elif city == 'dallas' or city == 'Dallas':
        lat0 = radians(32.8)
        lng0 = radians(-96.8)
    elif city == 'anchorage' or city == 'Anchorage':
        lat0 = radians(61)
        lng0 = radians(-150)

    lat1 = radians(lat1)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return int(distance)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
