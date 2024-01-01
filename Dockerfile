# set the base image
FROM apache/airflow:latest-python3.10

USER root
ARG AIRFLOW_USER_HOME=/opt/airflow
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}
WORKDIR ${AIRFLOW_HOME}
ENV PYTHONPATH “${AIRFLOW_USER_HOME}/dags”:“$PYTHONPATH”
COPY . ./

# basic installation
RUN apt-get update && apt-get -y install wget

# download and install chrome and chromedriver
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

# install requirements
USER airflow
RUN pip install pip --upgrade && pip install -r requirements.txt
RUN pip install protobuf==3.20.*
