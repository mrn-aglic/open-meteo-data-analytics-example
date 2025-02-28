#!/bin/sh

echo $1

if [ "$1" = 'scheduler' ]
then
    exec celery -A data_validation.beat beat --loglevel info
elif [ "$1" = 'worker' ]
then
    exec celery -A data_validation.worker worker -Q default --loglevel info
elif [ "$1" = 'flower' ]
then
    exec celery -A data_validation.worker --broker=redis://redis:6379/0 flower --conf=/config/flowerconfig.py
fi

exec "$@"
