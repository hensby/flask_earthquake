import sqlite3

import hello

if __name__ == '__main__':
    # dis = hello.get_distance_hav(34.0522342, -118.2436849)
    # print(dis)

    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    c = conn.cursor()
    c.execute("select * from all_month")
    # c.executescript("INSERT INTO distance VALUES ('nc73409661',1212,1223,232);")
    # "select * from all_month"
    data = c.fetchall()
    conn.close()

    conn = sqlite3.connect('test.db')
    print("Open database successfully")
    for row in data:
        id = str(row[0])
        dis_arlington = hello.get_distance_hav(int(float(row[2])), int(float(row[3])), 'arlington')
        dis_dallas = hello.get_distance_hav(int(float(row[2])), int(float(row[3])), 'dallas')
        dis_anchorage = hello.get_distance_hav(int(float(row[2])), int(float(row[3])), 'anchorage')

        sql = "INSERT INTO distance VALUES (?, ?, ?, ?)"
        c = conn.cursor()
        c.execute(sql, (id, dis_arlington, dis_anchorage, dis_dallas))
        conn.commit()
    conn.close()
#     (id, distance_from_Arlington, distance_from_Anchorage, distance_from_Dallas)
