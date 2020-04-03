#!/bin/bash

cd /home/m/LINUX2020/webscraper/lab/
source ./env/bin/activate >> /tmp/asdf.log 2>&1
./lab_project.py >> /tmp/asdf.log 2>&1
