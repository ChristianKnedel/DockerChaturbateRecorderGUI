#!/bin/bash
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
   export $variable_value
done

SIZE=$(du -sk /output/ | cut -f1)

if [[ $SIZE -gt 0 ]] && [[ $SIZE -gt $(($LIMIT_MAXIMUM_FOLDER_GB * 1024 * 1024)) ]]; then
    echo 'maximum size is reached'
    pkill -int ffmpeg &
fi