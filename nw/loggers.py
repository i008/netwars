import logstash
import logging
import sys
from nw.settings import ELK_HOST, LOGSTASH_PORT


def get_logger(lvl=logging.DEBUG):
    logger = logging.getLogger('nw-logger')
    logger.setLevel(lvl)

    logstash_handler = logstash.LogstashHandler(ELK_HOST, int(LOGSTASH_PORT))
    logstash_handler.setLevel(lvl)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    stdout_handler.setLevel(lvl)
    stdout_handler.setFormatter(stdout_formatter)

    # hdlr = logging.FileHandler('nwfilelog.log')
    # hdlr.setFormatter(stdout_formatter)
    # hdlr.setLevel(lvl)

    logger.addHandler(stdout_handler)
    logger.addHandler(logstash_handler)
    # logger.addHandler(hdlr)

    return logger


logger = get_logger()
