FROM        azelf/fc-ios-api-server
MAINTAINER  dev@azelf.com


COPY        . /srv/app
WORKDIR     /srv/app/front
RUN         npm install && \
            npm run build

COPY        .conf/uwsgi-app.ini /etc/uwsgi/sites/api-ios.ini
COPY        .conf/nginx-app.conf /etc/nginx/sites-available/api-ios
COPY        .conf/nginx.conf /etc/nginx/nginx.conf
COPY        .conf/supervisor-app.conf /etc/supervisor/conf.d/
RUN         ln -s /etc/nginx/sites-available/api-ios /etc/nginx/sites-enabled/api-ios
WORKDIR     /srv/app/django_app
EXPOSE      4567
CMD ["supervisord", "-n"]