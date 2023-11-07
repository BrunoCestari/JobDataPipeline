from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from docker.types import Mount


"""
DAG to extract Google Job data, load into AWS S3
"""



# Output name of extracted file. This be passed to each
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")


#Mapping the webscrape-container csv file to host machine (that is mapped to /opt/airflow/extraction)
code_dir = Mount(target='/tmp/raw_data',
                     source='/home/bccestari/Desktop/repos/JobDataPipeline/airflow/tmp',
                     type='bind')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0),
    'retries': 1,
}

dag = DAG(
    'Google_Job_Listings_Data_Pipeline',
    default_args=default_args,
    schedule_interval=None,  # Define your schedule interval
)

start_task = DummyOperator(task_id="start", dag=dag)

docker_task = DockerOperator(
    task_id='run_script_in_docker',
    image= 'webscrape-container',  # Replace with the correct image name
    api_version='auto',
    auto_remove=True,  # Remove the container when it's done
    docker_url='tcp://docker-proxy:2375',  # Remember it came from stackoverflow -> Very important
    command=["sudo", "python3", "webscrape.py", output_name],  # Command you want to execute in the container
    mounts = [code_dir],
    network_mode="bridge",  # Network mode to communicate with the host's Docker daemon
    dag=dag,
)

feature_engineering = BashOperator(
    task_id = "feature_engineering",
    bash_command = f"python3 /opt/airflow/extraction/feature_engineering.py {output_name}",
    dag = dag, 
)

upload_to_s3 = BashOperator(
    task_id="upload_to_s3",
    bash_command=f"python3 /opt/airflow/extraction/upload_aws_s3.py {output_name}",
    dag=dag,
)
upload_to_s3.doc_md = "Upload Google Jobs CSV data to S3 bucket"


start_task >> docker_task >> feature_engineering >> upload_to_s3
