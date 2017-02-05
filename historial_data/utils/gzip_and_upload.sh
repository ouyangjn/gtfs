#!/bin/sh
# compress historial data with gzip, except today's data
find /opt/oba/data -not -iname `date "+%Y.%m.%d".txt` -iname "*.txt" -exec gzip {} \;
# move *.gz files to AWS s3
find /opt/oba/data -iname "*.gz" -exec aws s3 mv {} s3://busgazer/historical_data/pittsburgh/ \;
