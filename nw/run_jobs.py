import time
from rq import Queue
from nw.jobs import scrape_topics
from nw.settings import redis_connection
from nw.loggers import logger

if __name__ == '__main__':
	# time.sleep(10)
	logger.debug("Starting adding jobs to Queues")
	topic_queue = Queue(connection=redis_connection, name='scrape_topics')
	topic_queue.enqueue(scrape_topics, kwargs={'topic_ids': [173521, 173446]})
