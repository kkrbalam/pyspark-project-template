from __future__ import print_function

import os
import sys
import traceback
from datetime import timedelta

import click
from pyhocon import ConfigTree

import logging
from cathay_configger import Configger
from cathay_time_utils import TimeUtils

from project_template.job.submit_job import SubmitJob

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
def receive(conf):
    logger.info("======== Start Submit Job ... ========")
    start = TimeUtils.get_now('ts')

    # load configs
    logger.info("Load configs...")
    try:
        confs = []
        for sub_conf in conf.split(':'):
            Configger.path(sub_conf)
            confs.append(Configger.get_config())
    except Exception:
        logger.error("Start Submit Job fail, please check your configurations.")
        exit(2)
    else:
        # merge configs
        logger.info("Merge configs...")
        configs = Configger.merge_configs(confs)

    try:
        current_env = os.environ['ENV']
        common_configs = configs.get('common', ConfigTree())
        env_configs = configs.get(current_env)
        merge_configs = Configger.merge_configs([common_configs, env_configs])
    except Exception:
        logger.error(traceback.format_exc())
        logger.error("Start Submit Job fail, find config by {} ENV error.".format(current_env))
        exit(2)

    logger.info(merge_configs.get("output.table"))
    # job
    logger.info("Start submit job...")
    try:
        submitJob = SubmitJob(config=merge_configs)
        submitJob.start()
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
