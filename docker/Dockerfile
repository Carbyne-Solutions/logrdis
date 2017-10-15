FROM alpine

LABEL maintainer="mdaue@carbyne.solutions"
LABEL reference="https://github.com/carbyne/logrdis"

ADD *.tar.gz /root

RUN apk update \
 && apk add python3 python3-dev yaml-dev ca-certificates \
 && pip3 install -U setuptools \
 && pip3 install /root/*

VOLUME ["/etc/logrdis"]

EXPOSE 4444

ENTRYPOINT ["/usr/bin/logrdis"]

CMD ["-c", "/etc/logrdis/logrdis.yml"]