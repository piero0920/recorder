#!/bin/bash

exec python3 /app/cron.py &
exec python3 /app/main.py