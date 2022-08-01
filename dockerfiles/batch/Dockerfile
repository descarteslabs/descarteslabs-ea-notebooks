FROM python:3.9-slim-buster

COPY app app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install -U descarteslabs>=1.11.0 

ENV DESCARTESLABS_ENV=aws-production

RUN mkdir /tmp/models

ENTRYPOINT ["python3", "-m", "app.dl_aws_batch"]