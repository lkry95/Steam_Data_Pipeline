import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

import dataCleaning

import os

from mysql.connector import (connection)

sql_pw = os.environ.get("MySqlPassword")

cnx = connection.MySQLConnection(user = 'root', password = 'sql_pw',
                                 host = 'localhost',
                                 database = 'Steam')
def get_data():

    page_url = "https://store.steampowered.com/search/?specials=1"

# opens the connection and downloads html page from url
    uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
# as if it were a json data type.
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()

# finds each product from the store page
    containers = page_soup.findAll("div",{"class":"responsive_search_name_combined"})

# name the output file to write to local disk
    out_filename = "steam_special_offers.csv"
# headers of csv file to be written
    headers = "Title,Release_Date,Reviews,Original_Price,Percent_Discount,Discounted_Price \n"


# opens file, and writes headers
    f = open(out_filename, "w")
    f.write(headers)

    contain = containers[0]
    container = containers[0]

# loops over each product and grabs attributes about
# each product

    for container in containers:

        title = container.span.text.replace(",",".")

        date_container = container.findAll("div", {"class": "col search_released responsive_secondrow"})
        release_date = date_container[0].text

        discountHolder = container.findAll("div", {"class": "col search_discount responsive_secondrow"})
        percent_discount = discountHolder[0].text.strip()

        try:
            reviews = (container.find('div', {'class': 'col search_reviewscore responsive_secondrow'}).span[
                       'data-tooltip-html'].split('<br>'))[0]
        except Exception as e:
            reviews = ''

        try:
            original_price = container.find('div', {'class': 'col search_price_discount_combined responsive_secondrow'}). \
                find('div', {'class': 'col search_price responsive_secondrow'}).text.strip()
        except Exception as e:
            try:
                original_price = container.find('div',
                                                {'class': 'col search_price_discount_combined responsive_secondrow'}). \
                    find('div', {'class': 'col search_price discounted responsive_secondrow'}).span.strike.text
            except Exception as e:
                original_price = ''

        PriceHolder = container.findAll("div", {"class": "col search_price discounted responsive_secondrow"})
        try:
             PriceHolder = PriceHolder[0].text
             PriceHolder = PriceHolder.split("$")
             discountedPrice = PriceHolder[-1]

        except IndexError:
        #     normalPrice = "Null";
             discountedPrice = original_price.strip('$')

            # prints the dataset to console
        print("title: " + title + "\n")
        print("release_date: " + release_date +"\n")



        f.write(title + ", " + release_date.replace(",", ".") + ", " + reviews + ", " + original_price + ", " + percent_discount + ", " + "$"+discountedPrice + "\n")

    f.close()  # Close the file
    dataCleaning.clean_data()

default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2020, 12, 9),
    'retries': 1,
    #allowed to retry workflow once if it fails with delay of 5 minutes
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('steam_scrape',
         default_args=default_args,
        #The DAG will run every day at 00:00 can also use '@daily' or '@hourly'
         schedule_interval='@daily',
         ) as dag:

    get_data = PythonOperator(task_id='get_data',
                                 python_callable=get_data)


cnx.close()



