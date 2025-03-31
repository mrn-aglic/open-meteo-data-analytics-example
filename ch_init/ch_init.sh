#!/bin/bash

echo "Running the SQL script to create the Weather table..."
ls -al /docker-entrypoint-initdb.d
clickhouse-client --query="$(cat /docker-entrypoint-initdb.d/air_quality.sql)"

echo "Air quality table created successfully!"
