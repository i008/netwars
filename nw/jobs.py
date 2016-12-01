import pyelasticsearch

from nw.loggers import logger
from nw.parser import NwParser
from nw.settings import ELK_HOST

nw_parser = NwParser(nw_date_parsing='beat')
es = pyelasticsearch.ElasticSearch('http://' + ELK_HOST)


def index_topics(topic_ids):
    logger.info('RUNNING RE-INDEX-SCRAPE JOB for topics: {}'.format(topic_ids))
    for topic_id in topic_ids:
        logger.info("Indexing topic {}".format(topic_id))
        posts_list = nw_parser.topic_to_json(topic_id)
        # logger.info(posts_list)
        es.bulk((es.index_op(p, id=p.get('unique_post_id')) for p in posts_list),
                index='nw', doc_type='post')
    return 1