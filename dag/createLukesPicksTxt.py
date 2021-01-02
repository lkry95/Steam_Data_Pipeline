#Creates Luke's Picks txt from picks table
import pymysql
import csv
import os

#new = pymysql.install_as_MySQLdb()

def create_Lukes_Picks():
    sql_pw = os.environ.get("MySqlPassword")

    user = 'root' # your username
    passwd = sql_pw # your password
    host = 'localhost' # your host
    db = 'Steam' # database where your table is stored
    table = 'picks' # table you want to save

    con = pymysql.connect(user=user, passwd=passwd, host=host, db=db)
    cursor = con.cursor()

    query = "SELECT Title FROM %s;" % table
    cursor.execute(query)

    with open('LukesPicks.txt','w') as f:
        writer = csv.writer(f)
        for row in cursor.fetchall():
            writer.writerow(row)