from nw.parser import NwParser
from sqlalchemy import create_engine
import pandas as pd
from nw.settings import NW_SQL_PATH, ELASTIC_HOSTS, ELK_HOST
import pyelasticsearch
from nw.loggers import logger

#
# def chunks(l, n):
#     for i in range(0, len(l), n):
#         yield l[i:i + n]
#
#
# if __name__ == '__main__':
#     es = pyelasticsearch.ElasticSearch('http://' + ELK_HOST)
#     engine = create_engine('sqlite:///{}'.format(NW_SQL_PATH))
#     df = pd.read_sql('select  topic_html from nwdump limit 100', engine)
#     parser = NwParser()
#
#     collect = []
#     failed = []
#     for i, topichtml in enumerate(df.topic_html.tolist()):
#         try:
#             topic_json = parser.topic_html_to_json(topic_html=topichtml)[0]
#         except:
#             failed.append(i)
#             continue
#         for post in topic_json:
#             collect.append(post)
#
#     docs = [es.index_op(d, id=d.get('unique_post_id')) for d in collect]
#     for i, chun in enumerate(chunks(docs, int(len(docs) * .05))):
#         logger.info('processing chunk {}'.format(i))
#         res = es.bulk(chun, index='nw', doc_type='post')
#         print(res)
#         print('---' * 10)
#         print(failed)
