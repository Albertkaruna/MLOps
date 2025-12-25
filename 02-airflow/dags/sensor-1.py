from airflow.sdk import dag, task
from airflow.providers.standard.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='filesystem_sensor_example',
    default_args=default_args,
    description='A simple DAG with FileSensor using decorators',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['example', 'sensor'],
)
def filesystem_sensor_dag():
    """
    Example DAG using FileSensor with TaskFlow API decorators
    """
    
    # Task 1: Wait for file to appear (sensors don't have decorators)
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/tmp/input_data.txt',  # File to wait for
        fs_conn_id='fs_default',
        poke_interval=10,  # Check every 10 seconds
        timeout=300,  # Timeout after 5 minutes (300 seconds)
        mode='poke',  # 'poke' keeps checking, 'reschedule' frees up worker slot
        soft_fail=False,  # If True, task will be skipped on timeout instead of failing
    )

    # Task 2: Process the file after it's found
    @task.bash
    def process_file():
        return 'echo "File found! Processing..." && cat /tmp/input_data.txt'

    # Task 3: Cleanup
    @task.bash
    def cleanup():
        return 'echo "Cleaning up..." && rm -f /tmp/input_data.txt'

    # Set task dependencies
    wait_for_file >> process_file() >> cleanup()

# Instantiate the DAG
filesystem_sensor_dag()