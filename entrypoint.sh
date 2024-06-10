#!/bin/bash
# Start the cron service
cron

cd root
# Start the Flask server
gunicorn --bind 0.0.0.0:80 src.api-server.app:app --workers 4 --threads 2 --timeout 0

