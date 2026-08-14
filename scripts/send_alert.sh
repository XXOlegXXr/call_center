#!/bin/bash

TO="oleghresko2006@gmail.com"

TYPE="$1"
MESSAGE="$2"

HOSTNAME=$(hostname)
DATE=$(date '+%Y-%m-%d %H:%M:%S')

SUBJECT="ASTERISK $TYPE"

BODY="
Asterisk Notification

Type: $TYPE
Server: $HOSTNAME
Time: $DATE

Message:
$MESSAGE
"

echo "$BODY" | mail -s "$SUBJECT" "$TO"
