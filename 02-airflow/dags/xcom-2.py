from airflow.sdk import dag, task

@dag
def xcom_dag_2():

    @task
    def task_a(ti):
        val='Karan'
        ti.xcom_push(key='my_key_1', value=val)

    @task
    def task_b(ti):
        val = ti.xcom_pull(task_ids='task_a',key='my_key_1')
        print(f"Value: {val}")

    task_a() >> task_b()

xcom_dag_2()