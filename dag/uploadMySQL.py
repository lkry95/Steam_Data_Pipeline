from sqlalchemy import create_engine
import os
import pandas as pd

def upload_MySQL():
    #Gets MySQL password from my local machine
    sql_pw = os.environ.get("MySqlPassword")
    #Reads csv to a dataframe
    df = pd.read_csv("/Users/luke/PassionProject/steam_special_offers.csv")
    #Create connection to MySQL database
    engine = create_engine("mysql+pymysql://root:{}@localhost/steam".format(sql_pw))

    #Drops yesterday's steam table
    connection = engine.raw_connection()
    cursor = connection.cursor()
    command = "DROP TABLE IF EXISTS {};".format('steam')
    cursor.execute(command)

    #uploads today's steam table
    df.to_sql('steam',con=engine, index=False)