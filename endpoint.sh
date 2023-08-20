#!/bin/bash
node --harmony /root/app/node-file-manager/lib/index.js -p 81 -d /root/app &
# python3 /root/app/main.py &
uvicorn main:app --host 0.0.0.0 --port 80 &
tail -f /dev/null