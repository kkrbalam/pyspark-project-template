from __future__ import print_function
from __future__ import unicode_literals

from pyspark.sql import SparkSession


def get_yarn_spark(app_name):
    # init spark session
    spark = SparkSession \
        .builder \
        .appName(app_name) \
        .master('local') \
        .enableHiveSupport() \
        .config('hive.exec.dynamic.partition.mode', 'nonstrict') \
        .config('spark.sql.parquet.compression.codec', 'uncompressed') \
        .getOrCreate()

    logger = spark.sparkContext._jvm.org.apache.log4j
    logger.LogManager.getLogger('org').setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger('akka').setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)

    return spark
