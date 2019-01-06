import os

from pyspark.sql import SparkSession

from cathay_spark import get_spark

from cathay.setting.config import load_config

import logging
logger = logging.getLogger(__name__)


def get_spark_session():
    config = load_config()

    # set app_name
    if os.environ['APP_TYPE'] == 'jupyter':
        app_name = config.get('jupyter.test.name')
    else:
        app_name = config.get('hippo.name')

    # set spark mode
    if os.environ['ENV'] == 'dev':
        mode = 'local'
    else:
        mode = 'yarn'

    # init spark session
    logger.info('get spark session, mode: {}'.format(mode))
    spark = get_spark(app_name, mode)

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
