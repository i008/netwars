import pickle
import time

import redis
from apscheduler.schedulers.blocking import BlockingScheduler

from nw.loggers import logger
from nw.parser import NwParser
from nw.settings import REDIS_HOST

scheduler = BlockingScheduler()


def beat():
    logger.info("Running BEAT {}".format(i))
    try:
        topic_status = pickle.loads(red_conn.get('topic_status'))
        user_status = pickle.loads(red_conn.get('user_status'))
    except pickle.UnpicklingError:
        logger.exception('Controlled fail of depickling')
        topic_status = user_status = None

    if not topic_status and not user_status:
        topics_new, list_of_users = nw.home_page_status()
        logger.debug(topics_new)
        logger.debug(list_of_users)
        if topics_new:
            red_conn.set('topic_status', pickle.dumps(topics_new))
        if list_of_users:
            red_conn.set('user_status', pickle.dumps(list_of_users))
        return

    elif topic_status and user_status:
        topics_new, users_new = nw.home_page_status()
        topic_diff = nw.topic_differences(topic_status, topics_new)
        users_diff = nw.live_user_differences(user_status, users_new)

        if topic_diff:
            # main task here
            red_conn.set('topic_status', pickle.dumps(topics_new))

        if users_diff:
            # main task here
            red_conn.set('topic_status', pickle.dumps(users_new))


class NetwarsBeat:
    def __init__(self, redis_connection, delay):
        self.redis = redis_connection
        self.delay = delay

    def _set_python_object_to_redis(self, python_object, key_name):
        status = self.redis.set(key_name, pickle.dumps(python_object))
        if not status:
            raise ValueError('Failed saving object in redis')

    def _get_python_object_from_redis(self, key_name):
        try:
            pickle.loads(self.redis.get(key_name))
        except pickle.UnpicklingError:
            logger.info('contro')


if __name__ == '__main__':
    time.sleep(3)
    red_conn = redis.StrictRedis(host=REDIS_HOST)
    nw = NwParser()
    scheduler.add_job(beat, 'interval', seconds=100)
    scheduler.start()
