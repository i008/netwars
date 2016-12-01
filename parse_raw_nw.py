import time
from itertools import zip_longest
from typing import Iterable

import begin
import grequests
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy import create_engine

from nw.loggers import logger
from nw.settings import DB_URI

MAX_TOPIC_NR = 173470
# TOPIC_RANGE_TO_SCRAPE = reversed(range(MAX_TOPIC_NR - 100, MAX_TOPIC_NR))
TOPIC_RANGE_TO_SCRAPE = reversed(range(MAX_TOPIC_NR))
NUMBER_TOPICS_PER_BATCH = 1
TIME_TO_SLEEP = 1


engine = create_engine(DB_URI)
metadata = MetaData(engine)

nw_raw = Table(
    'nwdump',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('topic_url', String),
    Column('topic_html', Text),
    Column('status_code', Integer)
)

nw_failed = Table(
    'nw_failed',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('url_failed', String)
)


def grouper(n: int, iterable: Iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def handle_exp(request, exception):
    logger.info('OH SHIT! failed to get {} \n exception: {}'.format(request.url, exception))
    conn.execute(nw_failed.insert(), {'url_failed': request.url})
    time.sleep(5)


def process_batch(url_range: Iterable) -> list:
    """
    :param url_range:
    :return:
    """
    prepared_requests = (grequests.get(url) for url in url_range)
    results = grequests.map(prepared_requests, exception_handler=handle_exp)
    # logger.info("batch processed")
    return filter(None, results)


def batch_to_db_format(batch_results):
    return [{'topic_url': r.url, 'topic_html': r.text, 'status_code': r.status_code}
            for r in batch_results if r]


@begin.start(auto_convert=True)
def run_scraper(sleep: 'Time to sleep between requests' = 1.0,
                nr_topics_per_batch: 'Number of topics scraped (async)' = 1):
    metadata.create_all()
    conn = engine.connect()
    grouped_urls_ids = list(grouper(nr_topics_per_batch, TOPIC_RANGE_TO_SCRAPE))
    for i, topic_ids in enumerate(grouped_urls_ids):
        if i % 10 == 0:
            logger.info("processed {} batches".format(i))
        time.sleep(sleep)
        res = process_batch([TOPIC.format(i) for i in topic_ids if i])
        batch_save = batch_to_db_format(res)
        conn.execute(nw_raw.insert(), batch_save)
