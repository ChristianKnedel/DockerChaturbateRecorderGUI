#!/bin/bash
export LANG=C.UTF-8
SIZE=$(du -sk /code/videos/ | cut -f1)

if [[ $SIZE -gt $MAXIMUM_FOLDER_KB ]]; then
    echo 'maximum size is reached'
    pkill -int ffmpeg &
    exit -1
fi

while getopts c: flag
do
    case "${flag}" in
        c) channel=${OPTARG};;
    esac
done


usermod -u $UID recorder
groupmod -g $GID recorder

if [ -z "$channel" ]
then
      echo "\$Incorrect channel name!"
fi

TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
OUTPUT=$(curl --referer "https://chaturbate.com" -s "https://chaturbate.com/api/chatvideocontext/${channel}/")

NAME=$(echo "${OUTPUT}" | eq ".broadcaster_username" )
SLUG=$(echo "${NAME}" | iconv -t ascii//TRANSLIT | sed -r s/[^a-zA-Z0-9]+/-/g | sed -r s/^-+\|-+$//g | tr A-Z a-z)
PLAYLIST_URL=$(echo "${OUTPUT}" | eq ".hls_source")

[ ! -d "/code/videos/${SLUG}" ] && mkdir -p "/code/videos/${SLUG}"
chown -R recorder:recorder "/code/videos/${SLUG}"
su recorder -c "ffmpeg -i ${PLAYLIST_URL} -c copy -bsf:a aac_adtstoasc /code/videos/${SLUG}/${SLUG}-${TIMESTAMP}.mp4" > /proc/1/fd/1 2>/proc/1/fd/2
