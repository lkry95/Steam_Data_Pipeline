#Configure common settings for all tasks
import datetime as dt

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

#Create Task
def print_world():
        print('world')

default_args = {
    'owner': 'me',
    'start_date': dt.datetime(2020, 11, 29),
    'retries': 1,
    #allowed to retry workflow once if it fails with delay of 5 minutes
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('airflow_tutorial_v01',
         default_args=default_args,
        #The DAG will run every day at 00:00 can also use '@daily' or '@hourly'
         schedule_interval='0 * * * *',
         ) as dag:

    # Task 1: print hello
    print_hello = BashOperator(task_id='print_hello',
                               bash_command='echo "hello"')
    # Task 2: wait 10 seconds
    sleep = BashOperator(task_id='sleep',
                         bash_command='sleep 5')
    # Task 3: print world
    print_world = PythonOperator(task_id='print_world',
                                 python_callable=print_world)

#Make chain of operations so dependencies do not get confused
print_hello >> sleep >> print_world