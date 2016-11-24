FROM continuumio/miniconda3
ADD . /etc/netwars
WORKDIR /etc/netwars
ENV PYTHONPATH="${PYTHONPATH}:/etc/netwars"
RUN pip install -r requirements.txt
