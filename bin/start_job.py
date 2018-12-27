from __future__ import print_function

import os
import sys
import traceback
from datetime import timedelta

import click
import papermill as pm

from cathay_time_utils import TimeUtils


reload(sys)
sys.setdefaultencoding('utf-8')

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def get_logger():
    from cathay_logger import Logger

    __log_config_path = 'conf/logging_config.ini'
    __app_type = os.environ['APP_TYPE']
    return Logger(__log_config_path).get_logger(__app_type, __name__)


logger = get_logger()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
@click.option('-a', '--app-home', help='app home')
def receive(conf, app_home):
    logger.info("======== Start Submit Job ... ========")
    start = TimeUtils.get_now('ts')

    # job
    logger.info("Start submit jupyter job...")
    try:
        date = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y-%m-%d')
        yyyymm = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y%m')
        db_tbl = 'test'
        pm.execute_notebook(
            '{}/jupyter_job/submit_job.ipynb'.format(app_home),
            '{}/jupyter_job/submit_job_{}.ipynb'.format(app_home, date),
            parameters=dict(yyyymm=yyyymm, db_tbl=db_tbl, conf=conf)
        )
    except Exception:
        logger.error(traceback.format_exc())
        exit(2)

    end = TimeUtils.get_now('ts')
    execution_time = end - start
    logger.info(
        "======== Successfully! Execution time: {} sec ========".format(execution_time))
    logger.info(
        "======== Execution time: {}  ========".format(timedelta(seconds=execution_time)))


if __name__ == '__main__':
    receive()
