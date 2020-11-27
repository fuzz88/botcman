FROM python:3.9-buster

LABEL maintainer="Ivan Oschepkov <ivan@oschepkov.ru>"

COPY requirements.txt /opt/

RUN pip install -r /opt/requirements.txt

COPY app/ /opt/app/
COPY entrypoint.sh /opt/

EXPOSE 8000

CMD ["sh", "/opt/entrypoint.sh"]