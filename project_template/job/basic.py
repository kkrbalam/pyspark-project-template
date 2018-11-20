from __future__ import print_function
from __future__ import unicode_literals

import logging
from cathay_spark import get_yarn_spark

logger = logging.getLogger(__name__)


class BasicJob(object):

    spark = None

    def __init__(self, config):
        self.config = config

        # hippo
        self.hippo_name = config.get('hippo.name')

    def _get_spark_session(self):
        logger.info('get spark session ...')
        self.spark = get_yarn_spark(self.hippo_name)

    def _close_spark_session(self):
        logger.info('close spark session ...')
        if self.spark is not None:
            self.spark.stop()
        else:
            logger.warn('No such spark session')
