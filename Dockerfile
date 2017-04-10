FROM        azelf/fc-ios-api-server
MAINTAINER  dev@azelf.com




COPY        . /srv/app
COPY        .conf/uwsgi-app.ini /etc/uwsgi/sites/api-ios.ini

COPY        .conf/nginx.conf /etc/nginx/nginx.conf
COPY        .conf/nginx-app.conf /etc/nginx/sites-available/api-ios

COPY        .conf/supervisord.conf /etc/supervisor/
COPY        .conf/supervisor-app.conf /etc/supervisor/conf.d/
RUN         rm -f /etc/nginx/sites-enabled/*
RUN         ln -s /etc/nginx/sites-available/api-ios /etc/nginx/sites-enabled/api-ios
RUN         mkdir -p /var/log/celery

WORKDIR     /srv/app/django_app
EXPOSE      4567
CMD ["supervisord", "-n"]