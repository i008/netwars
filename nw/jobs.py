from nw.parser import NwParser
# from nw.elastic_indexer import ElasticIndexerNW
from nw.loggers import logger
import time

nw_parser = NwParser()


def update_re_scrape_topics(topic_ids):
    logger.info('RUNNING RE-INDEX-SCRAPE JOB for topics: {}'.format(topic_ids))
    print('something rescrape')
    time.sleep(200)
    # es_indexer = ElasticIndexerNW()
    for topic_id in topic_ids:
        posts_list, topic_meta = nw_parser.topic_to_json(topic_id)
        # es_indexer.index_nw_topic(topic_meta)
        for post in posts_list:
            pass
        # es_indexer.index_nw_topic(post)


def update_re_scrape_users():
    _, users = nw_parser.home_page_status()
    return users


def test_job():
    print('doing bla job')
    time.sleep(10000)