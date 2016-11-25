from nw.parser import NwParser
# from nw.elastic_indexer import ElasticIndexerNW
from nw.loggers import logger

nw_parser = NwParser()


def scrape_topics(topic_ids):
    # es_indexer = ElasticIndexerNW()
    for topic_id in topic_ids:
        logger.info('interating trough topics {}'.format(topic_id))
        posts_list, topic_meta = nw_parser.topic_to_json(topic_id)
        # es_indexer.index_nw_topic(topic_meta)
        for post in posts_list:
            logger.info("iterating over posts {}".format(post))
            # es_indexer.index_nw_topic(post)


def scrape_users():
    _, users = nw_parser.home_page_status()
    return users




