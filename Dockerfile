FROM python:3.12-slim


RUN mkdir /app
WORKDIR /app/

ADD ./requirements/*.txt /app/requirements/

RUN apt-get -y update
RUN apt-get -y update && apt-get install -y \
    gcc \
    g++ \
    make \
    liblz4-dev \
    && rm -rf /var/lib/apt/lists/*


RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/requirements.txt

COPY . /app

LABEL name=celery-data-validation version=dev

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
