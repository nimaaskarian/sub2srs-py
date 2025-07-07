# sub2srs.py
**tl;dr**: its [sub2srs](https://sourceforge.net/projects/subs2srs/) but its a multiplatform script.

gets two subtitles (srt or lrc), a media file (video or audio, or anything that
ffmpeg supports) and makes media clips (any thing that ffmpeg supports) for each
subtitle section, and outputs it in csv for importing to anki.

# installation
the script depends on [ffmpeg](https://ffmpeg.org). install it. make sure its
available in your PATH (or on windows, is in the same directory as this script)

```
git clone https://github.com/nimaaskarian/sub2srs-py
cd sub2srs-py

# this will probably error in any distro that has python packages in its repo
# you probably can install python-srt from your repository, or use the
# --break-system-packages argument
pip3 install  -r requirements.txt
# link or copy to a directory inside your PATH.
ln $PWD/sub2srs.py /usr/bin
```
