# Netwars data and scraping


## What is it about:  
- Scrape all netwars.pl topics and store raw html in sql/elastic  
- Parse all raw html files into meaningfull json files and index them in Elasticsearch  
- Monitor netwars.pl for changes ->  scrape -> (re)index 
- A scheduled job will look for changes on the front page, once a change is detected, job to parse and index it will be send to RQ and processed by the worker pool.
- Visualize and explore the data in Pandas and Kibana

## Data:
- Around 5m posts where scraped and indexed in Elastic  
- Elastic data dump can be found here: **s3://i008/elkdata.7z**
- HDF5-PandasDataframe-Dump containing every post can be found here: **s3://i008/nw_posts.hdf5** 
- SQLite Dump cintaining every post can be found here: **s3://i008/nw_posts.sqlite**

Tables looks like that:   

|cites|forum_id|post_body|post_date|post_id|topic_id|topic_name|unique_post_id|user_id|user_name|0|1|2|3|4|
|--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |--- |
|[]|/forum/4|Dzisiaj rano wsiadając do auta spotkała mnie n...|2016-11-16 13:46:15|1|173469|[ZNPZ] Auto porysowane gowździem|173469-1|29243|Vol|
|[]|/forum/4|Jak nie ma kamer i nikt nic nie widział to rac...|2016-11-16 13:50:19|2|173469|[ZNPZ] Auto porysowane gowździem|173469-2|7201|Rocca|
|[]|/forum/4|Dzwon pod 666 podoficer Zupa|2016-11-16 13:51:45|3|173469|[ZNPZ] Auto porysowane gowździem|173469-3|18416|KiV|
|[173469-2]|/forum/4|i właśnie tak kombinuję, tym bardziej że kole...|2016-11-16 13:52:45|4|173469|[ZNPZ] Auto porysowane gowździem|173469-4|29243|Vol|
|[]|/forum/4|<fragment z pulp fiction jak Vince sie zali, z...|2016-11-16 13:54:20|5|173469|[ZNPZ] Auto porysowane gowździem|173469-5|15662|maac|

**shape: (5496160, 9)**

## Raw data:
There are some things to improve in parsing the data, the Raw-html dump of (almost) every topic can be found here:
**s3://i008/nwdb.sqlite**


## How to explore the data in Kibana
    - Dono twnload the dump elkdata.7z from S3 , unpack in main repo directory,
    ~ docker-compose up elk  
    - go to localhost:5601

Kibana example:
![](http://i.imgur.com/opjT4SH.png=300x "netwars kajbana")

## How to explore the data in Pandas:
```python
import pandas as pd
df = pd.read_hdf('posts_all.h5','posts') # few GB of memory needed
df.head()
```

## Deps:
- docker 
- check requirements.txt for all the rest

## Changelog:
- Last topic in dumps: /temat/173469

## Other
- U need to be authenticated on AWS to download the files from i008 bucket
- Sometimes ELK-Docker might fail starting  bc o host machine VM settings.
Usually this will help:

```bash
sudo sysctl -w vm.max_map_count=262144
```
