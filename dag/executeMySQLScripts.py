import pymysql
import os

def executeScripts():

    sql_pw = os.environ.get("MySqlPassword")

    user = 'root' # your username
    passwd = sql_pw # your password
    host = 'localhost' # your host
    db = 'Steam' # database where your table is stored
    table = 'picks' # table you want to save

    con = pymysql.connect(user=user, passwd=passwd, host=host, db=db)
    cursor = con.cursor()

    query1 = "DROP TABLE IF EXISTS picks;"
    query2 = "create table picks select * from Steam.steam where Title like '%Star Wars%' and Reviews like '%Positive%'or (`Discounted_Price ($)` = 0) or (Release_Date like '%2021%') or (Reviews = 'Overwhelmingly Positive' and `Percent_Discount (%)` >= 70);"
    cursor.execute(query1),cursor.execute(query2)