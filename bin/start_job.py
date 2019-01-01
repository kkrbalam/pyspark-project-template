from __future__ import print_function

import os
import sys
import re
import traceback
from datetime import timedelta

import click
from pyhocon import ConfigTree
import papermill as pm

from cathay_time_utils import TimeUtils
from cathay_configger import Configger


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
@click.option('-j', '--jupyter-conf', help='jupyter config')
@click.option('-a', '--app-home', help='app home')
def receive(conf, jupyter_conf, app_home):
    logger.info("======== Start Submit Job ... ========")
    start = TimeUtils.get_now('ts')

    # get jupyter config
    Configger.path(jupyter_conf)
    current_env = os.environ['ENV']
    jconf = Configger.get_config()
    jenv_configs = jconf.get(current_env)
    jcommon_configs = jconf.get('common', ConfigTree())
    jconfigs = Configger.merge_configs([jcommon_configs, jenv_configs])

    jupyter_dir = jconfigs.get('jupyter.job.dir')
    jexec_file = jconfigs.get('jupyter.job.exec_file')
    joutput_re = jconfigs.get('jupyter.job.output_re')
    joutput_prefix = jconfigs.get('jupyter.job.output_prefix')
    jkeep_history = jconfigs.get('jupyter.files.keep_history')

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

    # submit jupyter job
    logger.info("Start submit jupyter job...")
    try:
        date = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y-%m-%d')
        yyyymm = TimeUtils.cvt_datetime2str(TimeUtils.get_now('dt'), '%Y%m')
        db_tbl = 'test'
        pm.execute_notebook(
            os.path.join(jupyter_path, jexec_file),
            os.path.join(jupyter_path, '{}_{}.ipynb'.format(joutput_prefix, date)),
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
