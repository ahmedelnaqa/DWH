from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import tempfile
import os

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'spark_inline_test',
    default_args=default_args,
    description='Final Spark debug',
    schedule=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['spark', 'demo', 'final'],
) as dag:

    # Create the simplest possible script
    script_content = '''#!/usr/bin/env python3
import sys
import os

print("=" * 60)
print("MINIMAL SPARK EXECUTOR TEST")
print("=" * 60)
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    # Import only what we need
    from pyspark.sql import SparkSession
    
    # Create the most basic Spark session
    spark = SparkSession.builder \\
        .appName("MinimalTest") \\
        .master("spark://spark-master:7077") \\
        .config("spark.pyspark.python", sys.executable) \\
        .getOrCreate()
    
    print(f"SUCCESS: Spark session created! Version: {spark.version}")
    
    # Don't do any operations - just create and stop
    spark.stop()
    print("SUCCESS: Spark session stopped")
    sys.exit(0)
    
except Exception as e:
    print(f"ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
'''

    # Write to a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(script_content)
        temp_script_path = f.name

    spark_job = SparkSubmitOperator(
        task_id='run_minimal_spark',
        application=temp_script_path,
        conn_id='spark_default',
        verbose=True,
        deploy_mode='client',
        name='minimal-spark-debug',
        
        # MINIMAL configuration
        conf={
            'spark.master': 'spark://spark-master:7077',
            'spark.pyspark.driver.python': '/home/airflow/.local/bin/python3.12',
            'spark.pyspark.python': 'python3.12',  # Use command, not path
            'spark.driver.host': 'airflow-scheduler',
            'spark.driver.port': '4040',
            'spark.driver.bindAddress': '0.0.0.0',
        },
        
        application_args=[],
    )