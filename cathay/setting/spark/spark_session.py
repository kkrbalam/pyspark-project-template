import os

from cathay_spark import get_spark

from cathay.setting.config import load_config, get_full_keys

import logging
logger = logging.getLogger(__name__)


def get_spark_session():
    config = load_config()

    # set app_name
    app_name = config.get('hippo.name')

    if os.environ['APP_TYPE'] == 'jupyter':
        app_name = '{prefix}-{app_name}'.format(prefix=config.get('jupyter.test.prefix'), app_name=app_name)

    # set spark mode
    if os.environ['ENV'] == 'dev':
        mode = 'local'
    else:
        mode = 'yarn'

    # init spark session
    logger.info('get spark session, mode: {}'.format(mode))
    spark = get_spark(app_name, mode)

    # set spark configuration
    logger.info('set spark configuration ...')
    spark_configs = get_full_keys(config.get("spark", None), "spark")

    for k, v in spark_configs.items():
        logger.info("{} = {}".format(k, v))
        spark.conf.set(k, v)

    return spark


def close_spark_session(spark):
    logger.info('close spark session ...')

    if spark is not None:
        spark.stop()
    else:
        logger.warn('No such spark session')
