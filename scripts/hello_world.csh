#!/bin/csh
# By: Bartlomiej Mika
# Date: July, 16, 2015

# Clear all text on the screen
clear;

# Connect to local server
curl -H "Content-Type: application/json" -d '{"jsonrpc":"2.0","method":"hello_world","id":"1"}' http://127.0.0.1:8000/inventory/webservice/json

