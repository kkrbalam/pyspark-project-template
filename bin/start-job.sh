#!/bin/sh
export APP_HOME="$(cd "`dirname "$0"`"/..; pwd)"

. "${APP_HOME}"/libexec/log.sh

. "${APP_HOME}/conf/default.conf"
. "${APP_HOME}/conf/env.conf"
. "${APP_HOME}/conf/runtime-env-info.sh"
. "${APP_HOME}/libexec/run-py-venv.sh"

START_PATH=${APP_HOME}/bin/start_job.py

CONF_PATH_JOB=${APP_HOME}/conf/job.conf
CONF_PATH_HIPPO=${APP_HOME}/conf/hippo.conf
CONF_PATH=${CONF_PATH_JOB}:${CONF_PATH_HIPPO}

cd ${APP_HOME}

SPARK_JOB_NAME="example-job-name"

export APP_TYPE="job"

# from env.conf
export ENV=${ENV}


spark-submit \
    --name ${SPARK_JOB_NAME} \
    --master local \
    --conf spark.executorEnv.JAVA_HOME=/usr/java/jdk1.8.0_101/ \
    --conf spark.port.maxRetries=${SPARK_PORT_MAXRETRIES} \
    --executor-memory ${EXECUTOR_MEMORY} \
    --executor-cores ${EXECUTOR_CORES} \
    --num-executors ${NUM_EXECUTORS} \
    --driver-memory ${DRIVER_MEMORY} \
    --driver-cores ${DRIVER_CORES} \
    ${START_PATH} -c ${CONF_PATH}
