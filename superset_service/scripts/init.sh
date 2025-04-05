#!/usr/bin/bash

set -e

superset db upgrade

superset fab create-admin \
        --username admin \
        --email admin@superset.com \
        --password "$ADMIN_PASSWORD" \
        --firstname Superset \
        --lastname Admin

superset init

python /app/init_db_connections.py
