FROM ubuntu:20.04

# Set non-interactive frontend for APT
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y cron python3 python3-pip && \
    apt-get clean

COPY requirements.txt root/requirements.txt
RUN pip3 install -r root/requirements.txt

COPY src root/src

# Copy the crontab file into the cron.d directory
COPY cron-scheduler /etc/cron.d/cron-scheduler

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cron-scheduler

# Apply the cron job
RUN crontab /etc/cron.d/cron-scheduler

RUN touch /var/log/cron.log

COPY entrypoint.sh root/entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x root/entrypoint.sh

# Expose port 80 for Flask server
EXPOSE 80

ENTRYPOINT ["root/entrypoint.sh"]