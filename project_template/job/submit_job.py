from __future__ import print_function
from __future__ import unicode_literals

import logging
from basic import BasicJob
from cathay_time_utils import TimeUtils

logger = logging.getLogger(__name__)


class SubmitJob(BasicJob):

    def __init__(self, config):
        super(SubmitJob, self).__init__(config)

    def start(self):
        try:
            logger.info("=======test======")
            # get spark session
            self._get_spark_session()
            # ===  test start ===
            logger.info(TimeUtils.get_now())
            logger.info(self.config.get('hippo.name'))
            # ===  test end ===
            # TODO load config

            # TODO write code for the job

        except:
            raise
        finally:
            # close spark session
            self._close_spark_session()
