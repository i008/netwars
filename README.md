# Netwars data and scraping

## What is it about:  
1) Scrape all netwars.pl topics and store raw html in sql/elastic  

2) Parse all raw html files into meaningfull json files and index them in Elasticsearch  

3) Monitor netwars.pl for changes store raw content and index parsed in Elasticsearch.  

3) A scheduled job will look for changes on the front page, once a change is detected.   
A job to parse and index it will be send to RQ and processed by the worker pool (scrape->store>(re)index).  


## Data:
- Around 5m posts where scraped and indexed in Elastic  
Elastic data dump can be found here:  aws s3 cp elkdata.7z s3://i008/elkdata.7z  
HDF5-PandasDataframe-Dump containing every post can be found here: s3://i008/posts_all.h5  
It looks like that:
<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>cites</th>\n      <th>forum_id</th>\n      <th>post_body</th>\n      <th>post_date</th>\n      <th>post_id</th>\n      <th>topic_id</th>\n      <th>unique_post_id</th>\n      <th>user_href</th>\n      <th>user_name</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>0</th>\n      <td>[]</td>\n      <td>/forum/4</td>\n      <td>Dzisiaj rano wsiadając do auta spotkała mnie n...</td>\n      <td>2016-11-16 13:46:15</td>\n      <td>1</td>\n      <td>173469</td>\n      <td>173469.1</td>\n      <td>29243</td>\n      <td>Vol</td>\n    </tr>\n    <tr>\n      <th>1</th>\n      <td>[]</td>\n      <td>/forum/4</td>\n      <td>Jak nie ma kamer i nikt nic nie widział to rac...</td>\n      <td>2016-11-16 13:50:19</td>\n      <td>2</td>\n      <td>173469</td>\n      <td>173469.2</td>\n      <td>7201</td>\n      <td>Rocca</td>\n    </tr>\n    <tr>\n      <th>2</th>\n      <td>[]</td>\n      <td>/forum/4</td>\n      <td>Dzwon pod 666 podoficer Zupa</td>\n      <td>2016-11-16 13:51:45</td>\n      <td>3</td>\n      <td>173469</td>\n      <td>173469.3</td>\n      <td>18416</td>\n      <td>KiV</td>\n    </tr>\n    <tr>\n      <th>3</th>\n      <td>[post_2]</td>\n      <td>/forum/4</td>\n      <td>i właśnie tak kombinuję, tym bardziej że kole...</td>\n      <td>2016-11-16 13:52:45</td>\n      <td>4</td>\n      <td>173469</td>\n      <td>173469.4</td>\n      <td>29243</td>\n      <td>Vol</td>\n    </tr>\n    <tr>\n      <th>4</th>\n      <td>[]</td>\n      <td>/forum/4</td>\n      <td>&lt;fragment z pulp fiction jak Vince sie zali, z...</td>\n      <td>2016-11-16 13:54:20</td>\n      <td>5</td>\n      <td>173469</td>\n      <td>173469.5</td>\n      <td>15662</td>\n      <td>maac</td>\n    </tr>\n  </tbody>\n</table>'


## Deps:
- python 3.5+ only
check requirements.txt for other stuff

