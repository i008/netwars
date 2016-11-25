from rq import Worker, Queue, Connection
from nw.loggers import logger
from nw.settings import redis_connection

listen = ['high', 'default', 'low']


if __name__ == '__main__':
    with Connection(redis_connection):
        logger.info('starting workers')
        worker = Worker(map(Queue, listen))
        worker.work()