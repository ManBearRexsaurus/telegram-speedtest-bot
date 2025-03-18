FROM python:3.11-slim

RUN apt-get update && apt-get install -y cron

# Copy requirements.txt to the /app directory
COPY requirements.txt /app/

# Set the working directory to /app
WORKDIR /app

# Verify that requirements.txt is copied correctly
RUN ls -l /app/requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the /app directory
COPY telegram-speedtest-bot.py /app/
COPY .env /app/

# Set up cron schedule (runs hourly)
RUN echo "0 */12 * * * /usr/local/bin/python /app/telegram-speedtest-bot.py" > /etc/cron.d/telegram-speedtest-bot
RUN chmod 0644 /etc/cron.d/telegram-speedtest-bot
RUN crontab /etc/cron.d/telegram-speedtest-bot

# Start the cron daemon
CMD ["cron", "-f"]