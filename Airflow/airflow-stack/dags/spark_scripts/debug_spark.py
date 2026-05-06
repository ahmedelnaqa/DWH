#!/usr/bin/env python3
"""
Debug Spark execution
"""
import sys
import os

print("=" * 60)
print("DEBUG SCRIPT STARTING")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")
print(f"Environment variables:")
for key, value in os.environ.items():
    if 'PYTHON' in key or 'SPARK' in key or 'PATH' in key:
        print(f"  {key}={value}")

try:
    # Try to import pyspark
    import pyspark
    print(f"\nPySpark version: {pyspark.__version__}")
    
    # Try to create Spark context
    from pyspark import SparkContext
    
    # Create SparkContext with minimal configuration
    sc = SparkContext(
        appName="DebugApp",
        master="spark://spark-master:7077",
        conf={
            'spark.pyspark.driver.python': '/home/airflow/.local/bin/python3.12',
            'spark.pyspark.python': '/usr/bin/python3.12',
        }
    )
    
    print(f"SparkContext created successfully!")
    print(f"Master: {sc.master}")
    print(f"Application ID: {sc.applicationId}")
    
    # Try a simple operation
    data = [1, 2, 3, 4, 5]
    rdd = sc.parallelize(data)
    count = rdd.count()
    print(f"Simple RDD count: {count}")
    
    # Stop SparkContext
    sc.stop()
    print("\nSUCCESS: Spark debug completed!")
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)