FROM python:3.12-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    tzdata \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Install the required Python packages globally
RUN pip install --no-cache-dir redis flower

# Define environment variables for Python
ENV PYTHONUNBUFFERED=1 PYTHONHASHSEED=random PYTHONDONTWRITEBYTECODE=1

# Prepare app directories
RUN mkdir /app && mkdir /config

# Copy the flower config file and set permissions
COPY ./flower/flowerconfig.py /config/flowerconfig.py
RUN chmod +x /config/flowerconfig.py

# Copy the entire app to the container
COPY . /app

# Install requirements from the provided requirements.txt
WORKDIR /app/
ADD ./requirements/*.txt /app/requirements/
RUN pip install -r requirements/requirements.txt

ENV FLOWER_DATA_DIR /data
ENV PYTHONPATH ${FLOWER_DATA_DIR}

# Add a user with an explicit UID/GID and create necessary directories
RUN set -eux; \
    groupadd -g 1000 flower; \
    useradd -u 1000 -g flower flower; \
    mkdir -p "$FLOWER_DATA_DIR"; \
    chmod o+w "$FLOWER_DATA_DIR"; \
    chown flower:flower "$FLOWER_DATA_DIR"

# Switch to the flower user
USER flower

# Set working directory and data volume
WORKDIR /app
VOLUME $FLOWER_DATA_DIR

# Expose the default port
EXPOSE 5555

CMD ["celery", "flower"]
