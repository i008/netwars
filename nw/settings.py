import os
import redis

LOGGING_LEVEL = 'DEBUG'
NW_LOGIN = os.environ.get('nw_login', None)
NW_PASSWORD = os.environ.get('nw_pass', None)
ELK_HOST = 'localhost'
ELK_PORT = 9200
LOGSTASH_PORT = 5959
ELASTIC_HOSTS = [{'host': ELK_HOST,
                  'port': ELK_PORT}]

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
# redis_connection = redis.Redis(host=REDIS_HOST)
