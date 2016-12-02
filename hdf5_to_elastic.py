import pandas as pd
import pyelasticsearch
import begin

from nw.loggers import logger
from nw.settings import ELK_HOST

es = pyelasticsearch.ElasticSearch('http://' + ELK_HOST)


def index_posts_in_elastic(posts_df, batch_size=10000):
    batch = []
    for row in posts_df.iterrows():
        row = row[1].to_dict()
        if len(batch) <= batch_size:
            batch.append(es.index_op(row, id=row.get('unique_post_id')))
        else:
            logger.info('writing  batch')
            es.bulk(batch, index='nw', doc_type='post')
            batch = []
    es.bulk(batch, index='nw', doc_type='post')


@begin.start(auto_convert=True)
def main(batch_size=10000):
    posts_df = pd.read_hdf('nw_posts.hdf5', 'posts')
    index_posts_in_elastic(posts_df, batch_size=batch_size)
