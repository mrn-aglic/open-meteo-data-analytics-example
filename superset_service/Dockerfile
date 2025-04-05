FROM apache/superset:latest

ADD ./requirements/*.txt /app/requirements/

USER root

RUN apt-get update -y && \
    apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements/requirements.txt

USER superset
