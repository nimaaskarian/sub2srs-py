#!/usr/bin/sh

mkdir -p csv
pushd csv

# Download
wget https://downloads.tatoeba.org/exports/sentences.tar.bz2
wget https://downloads.tatoeba.org/exports/links.tar.bz2
wget https://downloads.tatoeba.org/exports/tags.tar.bz2
wget https://downloads.tatoeba.org/exports/sentences_with_audio.tar.bz2

# Decompress and untar
for f in *.tar.bz2; do
        tar jxf $f
done

# Prepare
sed 's/"/""/g;s/[^\t]*/"&"/g' sentences.csv > sentences.escaped_quotes.csv
sed 's/"/""/g;s/[^\t]*/"&"/g' tags.csv > tags.escaped_quotes.csv
uniq sentences_with_audio.csv > sentences_with_audio.uniq.csv

# Remove compressed files
rm -i *.tar.bz2

popd
