FROM apache/airflow:3.1.5

USER root

# System dependencies (optional, but production-safe)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Switch to airflow user for pip installs (REQUIRED)
USER airflow

RUN pip install --no-cache-dir \
    apache-airflow-providers-fab \
    apache-airflow-providers-apache-spark==5.5.0

# Back to root for runtime permissions
USER root
