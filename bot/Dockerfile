FROM python:3.9-buster

LABEL maintainer="Ivan Oschepkov <ivan@oschepkov.ru>"

COPY requirements.txt /opt/

RUN pip install --no-cache -r /opt/requirements.txt

COPY app/ /opt/app/
COPY entrypoint.sh /opt/
WORKDIR /opt/app/

CMD ["bash", "/opt/entrypoint.sh"]