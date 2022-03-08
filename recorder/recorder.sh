#!/bin/bash
while getopts u: flag
do
    case "${flag}" in
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
SLUG=$(echo "${NAME}" | iconv -t ascii//TRANSLIT | sed -r s/[^a-zA-Z0-9]+/-/g | sed -r s/^-+\|-+$//g | tr A-Z a-z)

PLAYLIST_URL=$(echo "${OUTPUT}" | grep m3u8 | grep -o -P '(?<=https://).*.m3u8')
CLEAN_PLAYLIST_URL=$(echo "${PLAYLIST_URL}" | sed "s/\\\u002D/-/g")
ffmpeg -i "https://${CLEAN_PLAYLIST_URL}" -c copy -bsf:a aac_adtstoasc  "/output/${SLUG}-${TIMESTAMP}.mp4"