#!/usr/bin/bash
log=/home/coast/ocean-report/olas/olas-cron.log
date +'%Y%m%d-%H%M%S' >> $log
python3 /home/coast/ocean-report/olas/olas_v1.1.py >> $log 2>&1
