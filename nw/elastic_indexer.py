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

    def index_nw_post(self, post_template):
        pass

    def index_nw_topic(self, topic):
        pass
