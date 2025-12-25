from airflow.sdk import PokeReturnValue, dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor
import os

@dag(dag_id='file_system_sensor_2', schedule=None, catchup=False)
def file_system_sensor_2():

    @task.sensor(poke_interval=30, timeout=300, mode='poke', soft_fail=True)
    def check_file_exist() -> PokeReturnValue:
        file_path = '/tmp/test.txt'
        
        if os.path.exists(file_path):
            print(f'File_found: {file_path}')
            return PokeReturnValue(is_done=True)
        else:
            print(f'File not found: {file_path}')
            return PokeReturnValue(is_done=False)
        
    @task.bash
    def read_file():
        return('echo "File content" && cat /tmp/test.txt')

    @task.bash
    def clean_file():
        return('echo "Cleaning the file" && rm -f /tmp/test.txt')

    check_file_exist() >> read_file() >> clean_file()

file_system_sensor_2()