import logstash
import logging
import sys
from nw.settings import ELK_HOST, LOGSTASH_PORT

logger = logging.getLogger('ds-logstash')
logger.setLevel(logging.DEBUG)

logstash_handler = logstash.LogstashHandler(ELK_HOST, int(LOGSTASH_PORT))
logstash_handler.setLevel(logging.DEBUG)

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(stdout_formatter)

logger.addHandler(stdout_handler)
logger.addHandler(logstash_handler)
