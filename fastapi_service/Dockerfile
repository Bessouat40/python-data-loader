FROM python:3.11.1

WORKDIR /

RUN apt-get update && apt-get install -y locales

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./api.py .
COPY ./main.py .
COPY ./postgresIngestor.py .

CMD python3 main.py