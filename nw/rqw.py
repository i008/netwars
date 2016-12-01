from rq import Worker, Queue, Connection
from nw.loggers import logger
from nw.nw_redis import NwRedis

listen = [
    'scrape_topics'
    # 'scrape_users'
]

if __name__ == '__main__':
    with Connection(NwRedis().redis_connection):
        logger.info('starting workers')
        worker = Worker(map(Queue, listen))
        worker.work()
