#!/bin/bash

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080)

echo "[$TIMESTAMP] code-server status: $RESPONSE" >> ~/health_check.log
