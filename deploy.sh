#!/bin/bash

# Set error handling
set -e

# Configuration
APP_DIR="/root/schizoposting"
VENV_DIR="$APP_DIR/venv"
GITHUB_REPO="https://github.com/ptitty12/schizoposting.git"  # Replace with your actual GitHub repo
LOG_FILE="$APP_DIR/deploy.log"
GUNICORN_PID_FILE="$APP_DIR/gunicorn.pid"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Navigate to the application directory
cd $APP_DIR

# Pull the latest changes from the GitHub repository
log_message "Pulling latest changes from GitHub..."
git pull origin main  # or your main branch name

# Activate virtual environment
source $VENV_DIR/bin/activate

# Install or update dependencies
log_message "Updating dependencies..."
pip install -r requirements.txt

# Update OpenAI and certifi libraries
log_message "Updating OpenAI and certifi libraries..."
pip install --upgrade openai certifi


log_message "Applying database migrations"
flask db upgrade

# Restart Gunicorn (only for this project)
log_message "Restarting Gunicorn for Schizoposting..."
if [ -f "$GUNICORN_PID_FILE" ]; then
    OLD_PID=$(cat "$GUNICORN_PID_FILE")
    if kill -0 $OLD_PID > /dev/null 2>&1; then
        kill $OLD_PID
        log_message "Stopped Gunicorn process $OLD_PID"
    else
        log_message "No running Gunicorn process found with PID $OLD_PID"
    fi
    rm "$GUNICORN_PID_FILE"
else
    log_message "No PID file found, assuming Gunicorn is not running"
fi


sleep 5
log_message "Starting Gunicorn..."
gunicorn --workers 3 --bind 127.0.0.1:5000 run:app --daemon \
    --pid "$GUNICORN_PID_FILE" \
    --access-logfile $APP_DIR/gunicorn_access.log \
    --error-logfile $APP_DIR/gunicorn_error.log \
    --timeout 120 --capture-output \
    --limit-request-line 0 \
    --limit-request-fields 55768 \
    --limit-request-field_size 0

# Check if Gunicorn started successfully
sleep 5
if [ -f "$GUNICORN_PID_FILE" ] && kill -0 $(cat "$GUNICORN_PID_FILE") > /dev/null 2>&1; then
    log_message "Gunicorn started successfully with PID $(cat "$GUNICORN_PID_FILE")"
else
    log_message "Failed to start Gunicorn. Check the error logs."
    exit 1
fi

log_message "Deployment completed!"
