#!/bin/bash
export LANG=C.UTF-8
SIZE=$(du -sk /code/videos/ | cut -f1)

if [[ $SIZE -gt 0 ]] && [[ $SIZE -gt $(($LIMIT_MAXIMUM_FOLDER_GB * 1024 * 1024)) ]]; then
    echo 'maximum size is reached'
    exit -1
fi

while getopts ":u:c:r:" o; do
    case "$o" in
        c) SLUG=${OPTARG};;
        u) URL=${OPTARG};;
        r) RESULUTION=${OPTARG};;
    esac
done


if [ -z "$url" ]
then
      echo "\$Incorrect URL!"
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

[ ! -d "/code/videos/${SLUG}" ] && mkdir -p "/code/videos/${SLUG}"
chown -R recorder:recorder "/code/videos/${SLUG}"
nice -n 19 ffmpeg -loglevel error -hide_banner -nostats -i ${URL} -s ${RESULUTION}  -c:a copy -c:v copy /code/videos/${SLUG}/${SLUG}-${TIMESTAMP}.mp4
