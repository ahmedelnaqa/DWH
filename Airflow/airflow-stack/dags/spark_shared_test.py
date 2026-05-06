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
    'spark_shared_volume_final',
    default_args=default_args,
    description='Final test with shared volume',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'shared', 'demo'],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id='run_shared_volume_spark',
        # Use the shared volume path
        application='/opt/shared/spark-scripts/shared_volume_test.py',
        conn_id='spark_default',
        verbose=True,
        deploy_mode='client',
        name='shared-volume-final',
        
        # Simple configuration
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.pyspark.driver.python': '/home/airflow/.local/bin/python3.12',
            'spark.pyspark.python': 'python3.12',
            'spark.driver.host': 'airflow-scheduler',
            'spark.driver.port': '7078',  # Different port to avoid conflicts
            'spark.driver.bindAddress': '0.0.0.0',
        },
        
        application_args=[],
    )