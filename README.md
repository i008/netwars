# netwars

What is it about:
1) Scrape all netwars.pl topics and store raw html in sql/elastic
2) Parse all raw html files into meaningfull json files and index them in Elasticsearch
3) Beat netwars.pl for changes store raw content and index parsed in Elasticsearch.
3.1) A scheduled job will look for changes on the front page, by monitoring the amount of posts each topic has,
once a change is detected. A job to parse and index it will be send to RQ and processed by the worker pool (scrape->store>(re)index).

