#!/bin/bash
cd /var/praekelt/yoza && \
source ve/bin/activate && \
cd yoza && \
python -W ignore manage.py stats_pageviews_csv --user-type mxit > ./stats/pageviews_mxit.csv && \
python -W ignore manage.py stats_pageviews_csv --user-type mobi > ./stats/pageviews_mobi.csv && \
python -W ignore manage.py stats_uniques_csv --user-type mxit > ./stats/uniques_mxit.csv && \
python -W ignore manage.py stats_uniques_csv --user-type mobi > ./stats/uniques_mobi.csv && \
python -W ignore manage.py cross_site_users_csv > ./stats/cross_site_users.csv && \
true