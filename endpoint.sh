#!/bin/bash
sudo node --harmony /root/app/node-file-manager/lib/index.js -p 81 -d /root/app &
# python3 /root/app/main.py &
sudo gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80 &> output.txt &