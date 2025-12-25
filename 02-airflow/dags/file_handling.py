from datetime import datetime
from airflow.sdk import dag, task

@dag(
    dag_id='file_handler',
    description='Simple file handling dag',
    schedule='@daily',
    start_date=datetime(2024,1,1),
    catchup=False,
    max_consecutive_failed_dag_runs=3,
    tags=['example','practice']
)
def file_handler():

    @task.bash
    def create_file():
        return "echo 'Hi There!' > /tmp/dummy.txt"
    
    @task.bash
    def check_file_exist():
        return "test -f /tmp/dummy.txt"

    @task
    def read_file():
        print(open('/tmp/dummy.txt', 'rb').read())
        
    create_file() >> check_file_exist() >> read_file()

file_handler()