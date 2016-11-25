from redis import Redis
from rq import Queue
from nw.jobs import scrape_topics
from nw.settings import redis_connection

topic_queue = Queue(connection=redis_connection)
topic_queue.enqueue(scrape_topics, kwargs={'topic_ids': [173521, 173446]})
