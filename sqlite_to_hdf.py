import datetime
import json
import sqlite3

import joblib
import pandas as pd
from pandas.io import sql

from nw.loggers import logger
from nw.parser import NwParser

parser = NwParser()
conn = sqlite3.connect('/media/i008/duzy1/nwdb.sqlite')


def t_to_json(html):
    try:
        return parser.topic_html_to_json(html)
    except:
        #         logger.info('--failed--')
        pass


select = conn.execute('SELECT topic_html FROM nwdump')
collect = []
ii = 0
for row in select:
    if not ii % 1000:
        logger.info('{} -- {}'.format(datetime.datetime.utcnow(), ii))
    collect.append(t_to_json(row[0]))
    ii += 1

joblib.dump(collect, 'all_posts_list.pickl')
flattened = [item for sublist in filter(None,collect) for item in sublist]
df = pd.DataFrame.from_records(flattened)
df.to_hdf('allposts_new', 'posts')

dx = df[:]
dx.cites = dx.cites.apply(lambda x: json.dumps(x))
dx.post_date = dx.post_date.astype(str)
cnx = sqlite3.connect('nw_posts.sqlite')
sql.to_sql(dx, 'nw_posts', cnx, if_exists='replace', chunksize=50000)
