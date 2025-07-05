#!/usr/bin/sh

mkdir -p output/audio

# Source: https://stackoverflow.com/a/11850469
./audio-urls.py -t $1 -d $2 | xargs -n 8 -P 8 wget --directory-prefix=output/audio/ --continue

cd output/audio
for f in *; do
        mv "$f" "tatoeba_${1}_${f}"
done
