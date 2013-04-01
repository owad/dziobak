#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn/dziobak.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3  #recommended formula here is 1 + 2 * NUM_CORES
 
#we don't want to run this as root..
USER=www-data
GROUP=www-data
 
source /home/owad/.virtualenvs/dziobak/bin/activate

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn_django -w $NUM_WORKERS 
  --debug
  --log-level=debug 
  --log-file=$LOGFILE 2>>$LOGFILE 
  --user=$USER --group=$GROUP
