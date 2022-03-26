#!/bin/bash
for variable_value in $(cat /proc/1/environ | sed 's/\x00/\n/g'); do
   export $variable_value
done

SIZE=$(du -sk /output/ | cut -f1)

echo "----- DEBUUG ------"
echo $SIZE
echo $MAXIMUM_FOLDER_KB


if [[ $SIZE -gt $MAXIMUM_FOLDER_KB ]]; then
    echo 'maximum size is reached'
    pkill -int ffmpeg &
fi