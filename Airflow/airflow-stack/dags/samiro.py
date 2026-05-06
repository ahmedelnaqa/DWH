from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def hello_airflow():
    print("✅ Hello Airflow! Your DAG is running successfully.")


with DAG(
    dag_id="samiro_demo_dag",
    description="Simple demo DAG for Airflow 3.x",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",   # ✅ FIXED
    catchup=False,
    tags=["demo", "test"],
) as dag:

    hello_task = PythonOperator(
        task_id="hello_airflow_task",
        python_callable=hello_airflow,
    )

    hello_task
