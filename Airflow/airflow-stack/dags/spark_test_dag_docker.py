from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'test_docker_spark_integration',
    default_args=default_args,
    description='Test Spark integration with Airflow bash',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo', 'spark'],
) as dag:

    test_spark_job = DockerOperator(
        task_id='run_spark_test',
        image='spark:4.1.0-py312New',  # Use an image with Spark & Python 3.12
        api_version='auto',
        auto_remove='success',
        command="""
        spark-submit \
        --master spark://spark-master:7077 \
        --conf spark.executor.memory=1g \
        --conf spark.driver.memory=1g \
        --name test-spark-job \
        --deploy-mode client \
        /opt/spark-app/example_spark_app.py
        """,
        docker_url='unix://var/run/docker.sock',
        network_mode='airflow-stack_default',  # <<< MUST match your Docker network
        environment={
            'PYSPARK_PYTHON': 'python3',
            'PYSPARK_DRIVER_PYTHON': 'python3'
        },
        mounts=[
            Mount(
                source='/absolute/path/to/your/local/airflow/dags/spark_scripts',
                target='/opt/spark-app',
                type='bind',
                read_only=True
            ),
        ]
    )