FROM python:3.7.5-buster

ADD . /app
WORKDIR /app

ARG PIP_EXTRA_INDEX_URL

RUN pip install --upgrade pip
RUN pip install -e .
RUN make reset-db

EXPOSE 6543
CMD ["make", "run-playground"]
