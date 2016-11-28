FROM sebp/elk
RUN rm /etc/logstash/conf.d/30-output.conf
ADD ls-conf.conf /etc/logstash/conf.d/ls-conf.conf

EXPOSE 5601
EXPOSE 9200
EXPOSE 5044
EXPOSE 5959/udp

