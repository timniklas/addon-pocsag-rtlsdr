#!/bin/bash

#get frequency from ha config
CONFIG_PATH=/data/options.json
FREQUENCY=$(jq --raw-output '.frequency // empty' $CONFIG_PATH)

rtl_fm -d 0 -f $FREQUENCY -s 22050 -g 100 | multimon-ng -t raw -a POCSAG1200 /dev/stdin | python3 -u /app/bosmon.py