FROM amsterdam/python:latest

RUN apt-get update \
	&& apt-get install -y \
	           mdbtools

RUN mkdir -p /data
RUN chmod 777 /data
#RUN chown datapunt /data


ADD requirements.txt /app

RUN pip install -r /app/requirements.txt
COPY . /app/

CMD /app/docker-run.sh
