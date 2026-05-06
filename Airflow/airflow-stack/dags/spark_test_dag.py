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
    'spark_integration_final',
    default_args=default_args,
    description='Complete Spark integration with Airflow',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'demo', 'production'],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id='run_spark_job',
        application='/opt/airflow/dags/spark_scripts/example_spark_app.py',
        conn_id='spark_default',
        verbose=True,
        deploy_mode='client',
        name='airflow-spark-job',
        
        # Configuration
        conf={
            # Memory settings
            'spark.executor.memory': '1g',
            'spark.driver.memory': '1g',
            
            # CRITICAL: Correct Python paths for your environment
            # Driver runs in Airflow container -> use Airflow's Python
            'spark.pyspark.driver.python': '/home/airflow/.local/bin/python3.12',
            # Executors run in Spark worker containers -> use Spark worker's Python
            'spark.pyspark.python': '/usr/bin/python3.12',
            
            # Network configuration
            'spark.driver.host': 'airflow-scheduler',
            'spark.driver.port': '4040',
            'spark.driver.bindAddress': '0.0.0.0',
            'spark.master': 'spark://spark-master:7077',
            
            # Port settings to avoid conflicts
            'spark.port.maxRetries': '50',
            'spark.blockManager.port': '4045',
            
            # Timeout settings
            'spark.network.timeout': '600s',
            'spark.executor.heartbeatInterval': '30s',
            
            # Dynamic allocation (optional but recommended)
            'spark.dynamicAllocation.enabled': 'true',
            'spark.dynamicAllocation.minExecutors': '1',
            'spark.dynamicAllocation.maxExecutors': '2',
            'spark.dynamicAllocation.initialExecutors': '1',
            
            # PySpark specific settings
            'spark.sql.execution.arrow.pyspark.enabled': 'true',
            'spark.sql.execution.arrow.pyspark.fallback.enabled': 'true'
            
            # Logging
            #'spark.eventLog.enabled': 'true',
            #'spark.eventLog.dir': 'file:///tmp/spark-events',
            #'spark.history.fs.logDirectory': 'file:///tmp/spark-events',
        },
        
        # Environment variables for the driver
        env_vars={
            'PYSPARK_PYTHON': '/usr/bin/python3.12',
            'PYSPARK_DRIVER_PYTHON': '/home/airflow/.local/bin/python3.12',
            # Add any other environment variables needed
        },
        
        application_args=[],
    )