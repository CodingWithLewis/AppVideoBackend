#!/bin/bash
# start.sh
ngrok config add-authtoken $NGROK_AUTH_TOKEN

# Start FastAPI server in the background
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Fetch the public URL from Ngrok and print it
ngrok http --domain=$NGROK_DOMAIN 8000 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
