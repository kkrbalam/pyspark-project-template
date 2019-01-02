from pyspark.sql import SparkSession

from cathay_spark import get_yarn_spark

from project_module.config import load_config

import logging
logger = logging.getLogger(__name__)


def get_spark_session():
    config = load_config()
    app_name = config.get('hippo.name')

    logger.info('get spark session')
    spark = get_yarn_spark(app_name)

    spark.conf.set("spark.executor.memory", config.get("spark.executor.memory"))
    spark.conf.set("spark.executor.cores", config.get("spark.executor.cores"))
    spark.conf.set("spark.num.executors", config.get("spark.num.executors"))
    spark.conf.set("spark.driver.memory", config.get("spark.driver.memory"))
    spark.conf.set("spark.driver.cores", config.get("spark.driver.cores"))
    spark.conf.set("spark.port.maxretries", config.get("spark.port.maxretries"))

    return spark


def close_spark_session(spark):
    logger.info('close spark session ...')

    if spark is not None:
        spark.stop()
    else:
        logger.warn('No such spark session')