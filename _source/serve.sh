#!/bin/sh
# (re)start the local preview server for ./site on port 8765
cd "$(dirname "$0")/site" || exit 1
nohup python3 -m http.server 8765 >/dev/null 2>&1 &
sleep 1
