#!/bin/bash

# Setting Protocol Buffers
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Start the FastAPI app in the background on port 8000
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start the Dash app on port 8050 using gunicorn in the background
gunicorn -w 4 -b :8050 "chat_app:server" --chdir /app &

# Start the litellm app on port 4000 using the specific config file path
litellm --config /app/config.yaml --port 4000 &

# Wait for any process to exit
wait -n

# Exit with status of the process that exited first
exit $?
