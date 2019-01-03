from __future__ import print_function

import os
import sys
import re
import traceback
import pickle
from datetime import timedelta

import click
from pyhocon import ConfigTree
import papermill as pm

import logging
from cathay_time_utils import TimeUtils
from cathay_configger import Configger

from cathay.config import merge_env_configs


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

    # get jupyter config
    jupyter_dir = configs.get('jupyter.job.dir')
    jexec_file = configs.get('jupyter.job.exec_file')
    joutput_re = configs.get('jupyter.job.output_re')
    joutput_prefix = configs.get('jupyter.job.output_prefix')
    jkeep_history = configs.get('jupyter.files.keep_history')

    if jkeep_history < 1:
        raise ValueError('jupyter history files should be at least 1')

    # rm old *.ipynb
    jupyter_path = os.path.join(app_home, jupyter_dir)
    regex = re.compile(joutput_re)
    match_files = filter(regex.match, os.listdir(jupyter_path))
    rm_files_amount = len(match_files) - jkeep_history
    if rm_files_amount > 0:
        for f in sorted(match_files)[:rm_files_amount]:
            logger.warning('rm old jupyter file: {}'.format(f))
            os.remove(os.path.join(jupyter_path, f))

    # save config to .pkl for jupyter to use
    config_pkl_path = configs.get('jupyter.config.save_pkl')
    with open(os.path.join(app_home, config_pkl_path), 'wb') as f:
        pickle.dump(configs, f)

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
