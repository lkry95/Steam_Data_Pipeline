#Configure common settings for all tasks
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import webscrapeData
import dataCleaning
import uploadMySQL
import executeMySQLScripts
import createLukesPicksTxt
import sendEmail

#Create Task

default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2021, 1, 2),
    'retries': 1,
    #allowed to retry workflow once if it fails with delay of 5 minutes
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('steam_data_pipeline',
         default_args=default_args,
        #The DAG will run every day at 00:00 can also use '@daily' or '@hourly'
         schedule_interval='@daily',
         ) as dag:

    # Task 1: print hello
    t1 = PythonOperator(task_id='extract_data_from_steam',
                               python_callable= webscrapeData.get_data)
    # Task 2: print world
    t2 = PythonOperator(task_id='clean_data',
                                 python_callable=dataCleaning.clean_data)

    t3 = PythonOperator(task_id='upload_data_MySQL',
                        python_callable=uploadMySQL.upload_MySQL)

    t4 = PythonOperator(task_id='create_new_table_with_SQL_script',
                        python_callable=executeMySQLScripts.executeScripts)

    t5 = PythonOperator(task_id='create_txt_file_with_game_suggestions',
                        python_callable=createLukesPicksTxt.create_Lukes_Picks)

    t6 = PythonOperator(task_id='send_email_with_txt_file',
                        python_callable=sendEmail.send_email)

#Make chain of operations so dependencies do not get confused
t1 >> t2 >> t3 >> t4 >> t5 >> t6