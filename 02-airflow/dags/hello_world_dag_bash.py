from datetime import datetime
from airflow.sdk import dag, task, chain
from airflow.providers.standard.operators.python import PythonOperator

@dag(
    dag_id="hello_world",
    description="My sample dag for hello world",
    schedule="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_consecutive_failed_dag_runs=3
)
def my_dag():

    @task
    def my_task_a():
        print("This is task_a task.")

    @task
    def my_task_b():
        print("This is task_b task.")

    @task
    def my_task_c():
        print("This is task_c task.")

    @task
    def my_task_d():
        print("This is task_d task.")

    @task
    def my_task_e():
        print("This is task_e task.")

    chain(my_task_a() >> [my_task_b(), my_task_d()], [my_task_c(), my_task_e()])

    # a = my_task_a()
    # a >> my_task_b() >> my_task_c()
    # a >> my_task_d() >> my_task_e()
    

my_dag()