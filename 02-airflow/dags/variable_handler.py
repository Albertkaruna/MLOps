from airflow.sdk import dag, task, Variable

@dag
def handle_variable():

    @task
    def print_variable():
        print(Variable.get('api', deserialize_json=True))

    print_variable()

handle_variable()
