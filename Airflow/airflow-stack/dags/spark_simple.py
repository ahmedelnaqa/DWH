from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'spark_simple',
    default_args=default_args,
    description='Debug Spark integration',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo', 'spark'],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id='debug_spark',
        application='/opt/airflow/dags/spark_scripts/debug_spark.py',
        conn_id='spark_default',
        verbose=True,
        deploy_mode='client',
        name='spark-debug-job',
        
        # ABSOLUTE MINIMUM configuration
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.pyspark.driver.python': '/home/airflow/.local/bin/python3.12',
            'spark.pyspark.python': '/usr/bin/python3.12',
        },
        
        application_args=[],
    )