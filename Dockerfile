FROM continuumio/miniconda3
ADD . /opt/netwars
WORKDIR /opt/netwars
RUN pip install -r requirements.txt
