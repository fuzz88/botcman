FROM python:3.9-alpine

LABEL maintainer="Ivan Oschepkov <ivan@oschepkov.ru>"

COPY requirements.txt /opt/

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
	&& pip install -r /opt/requirements.txt \
	&& apk del .build-deps

COPY app/ /opt/app/
COPY entrypoint.sh /opt/

CMD ["sh", "/opt/entrypoint.sh"]