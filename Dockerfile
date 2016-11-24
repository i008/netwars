FROM continuumio/miniconda3
ADD . /etc/netwars
WORKDIR /etc/netwars
RUN pip install -r requirements.txt
RUN pip install redis