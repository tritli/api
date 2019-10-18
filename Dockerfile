FROM python:3.6

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev libatlas-base-dev gfortran nginx supervisor

RUN pip3 install uwsgi

COPY ./requirements.txt /project/requirements.txt
RUN python3 -m pip install -r /project/requirements.txt

RUN useradd --no-create-home nginx

#RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY /docker/nginx.conf /etc/nginx/
COPY /docker/flask-site-nginx.conf /etc/nginx/conf.d/
COPY /docker/uwsgi.ini /etc/uwsgi/
COPY /docker/supervisord.conf /etc/

COPY /src /project

WORKDIR /project

EXPOSE 80

CMD ["/usr/bin/supervisord"]
