import os
import traceback

from pyhocon import ConfigTree

import logging
from cathay_configger import Configger

logger = logging.getLogger(__name__)


def merge_env_configs(conf):
    # load configs
    logger.info("Load configs...")
    try:
        confs = []
        for sub_conf in conf.split(':'):
            Configger.path(sub_conf)
            confs.append(Configger.get_config())
    except Exception:
        logger.error("Start Submit Job fail, please check your configurations.")
        raise

    else:
        # merge configs
        logger.info("Merge configs...")
        configs = Configger.merge_configs(confs)

    try:
        current_env = os.environ['ENV']
        common_configs = configs.get('common', ConfigTree())
        env_configs = configs.get(current_env)
        merge_configs = Configger.merge_configs([common_configs, env_configs])
        return merge_configs
    except Exception:
        logger.error(traceback.format_exc())
        logger.error("Start Submit Job fail, find config by {} ENV error.".format(current_env))
