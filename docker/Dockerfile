FROM alpine

LABEL maintainer="mdaue@carbyne.solutions"
LABEL reference="https://github.com/carbyne/logrdis"

ADD *.tar.gz /root

RUN apk update \
 && apk add python3 python3-dev libyaml \
 && pip install /root/*.tar.gz

VOLUME ["/etc/logrdis"]

EXPOSE 4444

ENTRYPOINT ["/usr/local/bin/logrdis"]

CMD ["-c", "/etc/logrdis/logrdis.yml"]