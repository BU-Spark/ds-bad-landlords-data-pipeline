#!/bin/bash
# Start the cron service
cron

cd root

# Run the script immediately
echo "$(date) - First data pipeline run" >> /root/logfile.log 2>&1 && python3 /root/src/main.py >> /root/logfile.log 2>&1

# Start the Flask server
gunicorn --bind 0.0.0.0:80 src.api-server.app:app --workers 4 --threads 2 --timeout 0