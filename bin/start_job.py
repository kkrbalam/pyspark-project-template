import os
import sys
import traceback
import pickle
from datetime import timedelta

import click
import papermill as pm

import logging
from cathay_time_utils import TimeUtils
from cathay_configger import Configger

from cathay.config import merge_env_configs
from cathay.jupyter import get_jupyter_dir, rm_jupyter_history, dump_configs


reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-c', '--conf', help='config')
def receive(conf):
    logger.info("======== Start Submit Job ... ========")
    start = TimeUtils.get_now('ts')

    # get app home
    app_home = os.environ['APP_HOME']

    # merge all configs
    configs = merge_env_configs(conf)

    try:
        # rm old jupyter *.ipynb
        rm_jupyter_history(configs, app_home)

        # dump config to .pkl for jupyter to use
        dump_configs(configs, app_home)

        # get jupyter config
        jupyter_path = get_jupyter_dir(configs, app_home)
        jexec_file = configs.get('jupyter.job.exec_file')
        joutput_prefix = configs.get('jupyter.job.output_prefix')

    except Exception:
        logger.error(traceback.format_exc())
        exit(2)

    # submit jupyter job
    logger.info("Start submit jupyter job...")
    try:
        date = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y-%m-%d')
        yyyymm = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y%m')
        db_tbl = 'test'
        pm.execute_notebook(
            os.path.join(jupyter_path, jexec_file),
            os.path.join(jupyter_path, '{}_{}.ipynb'.format(joutput_prefix, date)),
            parameters=dict(yyyymm=yyyymm, db_tbl=db_tbl)
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
