#!/bin/bash

TO="oleghresko2006@gmail.com"
SUBJECT="$1"
BODY="$2"

echo "$BODY" | mail -s "$SUBJECT" "$TO"
