from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'test_bash_spark_integration',
    default_args=default_args,
    description='Test Spark integration with Airflow bash',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo', 'spark'],
) as dag:
    
    test_spark_job = BashOperator(
        task_id='run_spark_test',
        bash_command="""
        "PYSPARK_PYTHON=python3.12 PYSPARK_DRIVER_PYTHON=python3.12 \
   spark-submit --master spark://spark-master:7077 --deploy-mode client \
   /opt/airflow/dags/spark_scripts/example_spark_app.py"
        """,
        env={
            'PYSPARK_PYTHON': 'python3.12',  # Changed to python3.12
            'PYSPARK_DRIVER_PYTHON': 'python3.12'  # Changed to python3.12
        }
    )