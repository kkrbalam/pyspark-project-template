#echo "this script is for runtime environment check "

# what might be interested:
# network
# memory
# build path
# dependency
# whoami
# service version, like Impala, Hive, HBase....
# language version, like Python, JDK, R, Scala


if [[ "${ENV}" == "prod" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/source/hadoop/conf
    export SPARK_HOME=/etc/spark-2.3.1-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH

elif [[ "${ENV}" == "uat" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/source/hadoop/conf
    # export SPARK_HOME=/etc/spark-2.3.1-bin-hadoop2.6
    export SPARK_HOME=/usr/local/spark-2.1.0-bin-hadoop2.7
    export PATH=$SPARK_HOME/bin:$PATH

elif [[ "${ENV}" == "ut" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=/etc/hadoop/conf
    export SPARK_HOME=/opt/spark-2.1.0-bin-hadoop2.6
    export PATH=$SPARK_HOME/bin:$PATH

elif [[ "${ENV}" == "dev" ]]; then
    # == HADOOP + SPARK ==
    export HADOOP_CONF_DIR=
    export SPARK_HOME=/usr/local/spark-2.1.0-bin-hadoop2.7
    export PATH=$SPARK_HOME/bin:$PATH

else

    log_info "ENV: '${ENV}' not found!"
    exit 2

fi
