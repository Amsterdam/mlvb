FROM amsterdam/docker_python:latest

RUN apt-get update \
	&& apt-get install -y \
	           mdbtools

RUN mkdir -p /data
RUN chmod 777 /data
#RUN chown datapunt /data


ADD requirements.txt /app

RUN pip install -r /app/requirements.txt
COPY . /app/

#USER datapunt

#WORKDIR /app

# run the import (TBD: still relevant?)
CMD /app/docker-run.sh
