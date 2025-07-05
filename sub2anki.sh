#!/usr/bin/env bash
# a simple script to generate anki files from mkv video sources

dir=$(dirname $0)
# read langs to array `langs`
readarray -t langs < <(ffmpeg -i "$1" 2>&1 | grep 'Stream.*Subtitle:' | cut -d : -f 2 | sed 's/.*(\(.*\)).*/\1/')
# declare a hashmap `lang_files`
declare -A lang_files
base=tmp.$(date +%s).sub2anki
# map files of a hashmap to a tmp.date.<epoch>.sub2anki.<lang>.srt
for key in "${!langs[@]}"; do
  lang=${langs[$key]}
  [ -z "${lang_files[$lang]}" ] && {
    tmp=/tmp/$base-${lang}.srt
    ffmpeg -i "$1" -map "0:s:$key" "$tmp"
    lang_files[$lang]=$tmp
  }
done
"$dir/sub2anki.py" --source "${lang_files[0]}" --target "${lang_files[1]}" --media "$1" "${!lang_files[0]}2${!lang_files[1]}.csv"
