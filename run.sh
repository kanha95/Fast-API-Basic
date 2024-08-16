#!/bin/bash

# Kill the processes listed in save_pids.txt
if [ -f /home/ubuntu/Fast_API/save_pids.txt ]; then
  xargs kill -9 < /home/ubuntu/Fast_API/save_pids.txt
  rm /home/ubuntu/Fast_API/save_pids.txt
fi

source /home/ubuntu/myenv/bin/activate

# Execute the command in the background, redirect output and errors to my.log
nohup gunicorn main:app --chdir /home/ubuntu/Fast_API --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:7861 > /home/ubuntu/Fast_API/nohup.out 2>&1 &

# Wait a moment to ensure all workers are started
sleep 2

lsof /home/ubuntu/Fast_API/nohup.out | awk '/gunicorn/ {print $2}' | sort -u > /home/ubuntu/Fast_API/save_pids.txt
