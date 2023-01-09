#!/bin/bash
date >> ~/BigApplePI/data_cron.txt
python3 ~/BigApplePI/pipeline.py >> ~/BigApplePI/data_cron.txt 2>&1
echo " " >> ~/BigApplePI/data_cron.txt
