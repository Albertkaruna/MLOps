from airflow.sdk import dag, task

@dag
def xcom_dag_3():

    @task
    def task_a():
        val='Karunakaran'
        return val

    @task
    def task_b(my_val: str):
        val = my_val
        print(f"Value: {val}")

    val = task_a()
    task_b(val)

xcom_dag_3()