#!/bin/bash
cd /var/praekelt/yoza/yoza && \
	source ../ve/bin/activate && \
	./manage.py send_mail >> /var/praekelt/yoza/yoza/cron_mail.log 2>&1

