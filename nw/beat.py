from apscheduler.jobstores.redis import RedisJobStore
# from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
from pytz import utc
import redis
import time
from nw.loggers import logger
from nw.parser import NwParser
import pickle


scheduler = BlockingScheduler()


def set_python_object_to_redis(obj, key_name):
    red_conn.set(key_name, pickle.dumps(obj))


def get_python_object_form_redis(key_name):
    pass


def beat():
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
        topic_diff = nw._topic_differences(topic_status, topics_new)
        users_diff = nw._live_user_differences(user_status, users_new)

        if topic_diff:
            # main task here
            red_conn.set('topic_status', pickle.dumps(topics_new))

        if users_diff:
            # main task here
            red_conn.set('topic_status', pickle.dumps(users_new))


if __name__ == '__main__':
    time.sleep(3)
    red_conn = redis.StrictRedis(host='redis')
    nw = NwParser()
    scheduler.add_job(beat, 'interval', seconds=100)
    scheduler.start()
