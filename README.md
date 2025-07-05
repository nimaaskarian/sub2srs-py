a collection of anki deck generation tools

# sub2anki.py
**tl;dr**: its sub2anki but written in python with *nix systems in mind.

gets two subtitles (srt or lrc), a media file (video or audio, or anything that
ffmpeg supports) and makes media clips (any thing that ffmpeg supports) for each
subtitle section, and outputs it in csv for importing to anki.

## sub2anki.sh
extracts subtitles from mkv files and run [sub2anki.py](#sub2anki-py) with them.

# tatoeba
there's a directory called tatoeba, which is a tool set to download sentences
from tatoeba and convert them to anki cards.

