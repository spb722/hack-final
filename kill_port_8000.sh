#!/bin/bash

PORT=8000

echo "Finding processes running on port $PORT..."

# Get PIDs of processes using port 8000
PIDS=$(lsof -ti :$PORT)

if [ -z "$PIDS" ]; then
    echo "No processes found running on port $PORT"
    exit 0
fi

echo "Found processes with PIDs: $PIDS"
echo "Killing processes..."

# Kill the processes
for PID in $PIDS; do
    echo "Killing process $PID"
    kill -9 $PID
done

echo "All processes on port $PORT have been killed"