import redis
import pickle
from nw.loggers import logger
from nw.settings import REDIS_HOST


class NwRedis:
    def __init__(self, redis_host=REDIS_HOST):
        self.redis_connection = redis.Redis(host=redis_host)

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass

    def set_python_object_to_redis(self, python_object, key_name):
        status = self.redis_connection.set(key_name, pickle.dumps(python_object))
        if not status:
            raise ValueError('Failed saving object in redis')

    def get_python_object_from_redis(self, key_name):
        try:
            return pickle.loads(self.redis_connection.get(key_name))
        except:
            logger.exception('Controlled fail to retrive python obj from redis')
            return None

    def save_topics_to_redis(self, topics_status):
        self.set_python_object_to_redis(topics_status, 'topic_status')

    def save_users_to_redis(self, user_status):
        self.set_python_object_to_redis(user_status, 'user_status')

    def get_users_from_redis(self):
        return self.get_python_object_from_redis('user_status')

    def get_topics_from_redis(self):
        return self.get_python_object_from_redis('topic_status')
