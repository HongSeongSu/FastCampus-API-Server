FROM        azelf/fc-ios-api-server
MAINTAINER  dev@azelf.com



EXPOSE      4567
CMD ["supervisord", "-n"]