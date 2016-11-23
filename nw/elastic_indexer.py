from nw.settings import ELASTIC_HOSTS
import elasticsearch
import datetime


class ElasticIndexerNW:
    def __init__(self):
        self.es = elasticsearch.Elasticsearch(hosts=ELASTIC_HOSTS)

    def index_raw_topic_html(self, topic_html, topic_url, status_code, index='rawnw'):
        unique_id = int(topic_url.split('/')[-1])
        self.es.index(
            index=index,
            doc_type='raw',
            id=unique_id,
            body={
                'topic_html': topic_html,
                'topic_url': topic_url,
                'status_code': status_code,
                'date_indexed': datetime.datetime.utcnow()
            })

    def index_nw_post(self, nw_post_dict):
        self.es.index(
            index='nw',
            doc_type='post',
            id=nw_post_dict['unique_post_id'],
            body=nw_post_dict
        )

    def index_nw_topic(self, nw_topic_dict):
        self.es.index(
            index='nw',
            doc_type='topic',
            id=nw_topic_dict.get('topic_id'),
            body=nw_topic_dict
        )

    def index_active_users(self, nw_active_users):
        pass
        # timenow = datetime.datetime.utcnow()
