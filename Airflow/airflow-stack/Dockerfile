ARG AIRFLOW_VERSION=3.1.6
FROM apache/airflow:${AIRFLOW_VERSION}

USER root

# Install Java + tools
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     openjdk-17-jre-headless wget ca-certificates tar \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Versions aligned with Airflow constraints
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV SPARK_VERSION=4.1.0
ENV SPARK_DIST=spark-${SPARK_VERSION}-bin-hadoop3
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:${SPARK_HOME}/bin

# Install Spark client
RUN mkdir -p /opt && \
    cd /opt && \
    wget -q https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_DIST}.tgz && \
    tar -xzf ${SPARK_DIST}.tgz && \
    mv ${SPARK_DIST} ${SPARK_HOME} && \
    rm ${SPARK_DIST}.tgz && \
    chown -R airflow:root ${SPARK_HOME}

USER airflow

# Install Python deps using Airflow constraints
RUN pip install --no-cache-dir \
    apache-airflow-providers-apache-spark \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-3.12.txt"

USER root

# Make spark-submit globally available
RUN ln -sf ${SPARK_HOME}/bin/spark-submit /usr/local/bin/spark-submit

USER airflow
