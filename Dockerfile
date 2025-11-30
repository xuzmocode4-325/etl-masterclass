# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Environment variables for Airflow version and Python version
ENV AIRFLOW_VERSION=3.1.3
ENV PYTHON_VERSION=3.10
ENV CONSTRAINT_URL=https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt

# Install Airflow with Celery extra and constraints for reproducible install
COPY 
RUN pip install "apache-airflow[celery]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Create Airflow user and directories
RUN useradd -ms /bin/bash airflow
USER airflow
WORKDIR /home/airflow
RUN mkdir dags logs plugins

ENV AIRFLOW_HOME=/home/airflow

# Expose port for webserver
EXPOSE 8080

# Default command to run Airflow webserver
CMD ["airflow", "api-server"]
