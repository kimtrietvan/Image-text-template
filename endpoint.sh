#!/bin/bash
node --harmony /root/app/node-file-manager/lib/index.js -p 81 -d /root/app &
python3 /root/app/main.py &
tail -f /dev/null