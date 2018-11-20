#echo "this script is for runtime environment check "

# what might be interested:
# network
# memory
# build path
# dependency
# whoami
# service version, like Impala, Hive, HBase....
# language version, like Python, JDK, R, Scala

# == HADOOP + SPARK ==
export HADOOP_CONF_DIR=
export SPARK_HOME=/usr/local/spark-2.3.0-bin-hadoop2.6
export PATH=$PATH:$SPARK_HOME/bin

export PYTHONPATH=${PYTHONPATH}:${APP_HOME}/src
export PYTHONPATH=${PYTHONPATH}:${APP_HOME}/conf