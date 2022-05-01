#!/bin/bash
export LANG=C.UTF-8
SIZE=$(du -sk /code/videos/ | cut -f1)

if [[ $SIZE -gt 0 ]] && [[ $SIZE -gt $(($LIMIT_MAXIMUM_FOLDER_GB * 1024 * 1024)) ]]; then
    echo 'maximum size is reached'
    exit -1
fi

while getopts ":u:c:" o; do
    case "$o" in
        c) SLUG=${OPTARG};;
        u) url=${OPTARG};;
    esac
done


if [ -z "$url" ]
then
      echo "\$Incorrect URL!"
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUTPUT=$(curl "${url}")

NAME=$(echo "${OUTPUT}}" | grep 'og:title' | grep -E "Watch (.*?) live on Chaturbate!" | sed 's/.*Watch\s\(.*\)\slive\son\sChaturbate.*/\1/')

PLAYLIST_URL=$(echo "${OUTPUT}" | grep m3u8  | sed "s/\\\u002D/-/g" | grep -o 'https://[a-zA-Z0-9.+-_:/]*.m3u8')
[ ! -d "/code/videos/${SLUG}" ] && mkdir -p "/code/videos/${SLUG}"
chown -R recorder:recorder "/code/videos/${SLUG}"
ffmpeg -loglevel error -hide_banner -nostats -i ${PLAYLIST_URL} -c copy -bsf:a aac_adtstoasc  /code/videos/${SLUG}/${SLUG}-${TIMESTAMP}.mp4
