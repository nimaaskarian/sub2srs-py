#!/usr/bin/env python3
import os
from datetime import timedelta
from argparse import ArgumentParser, FileType

def main(args):
    import csv
    writer = csv.writer(args.output_csv)
    for i, (sub1, sub2) in enumerate(subtitles(args)):
        start = min((sub1.start, sub2.start))
        end = max((sub1.end, sub2.end))
        print(str(start), str(end))
        base, _ = os.path.splitext(os.path.basename(args.media))
        name=f"2srts2anki_{base}_{i+1}.{args.audio_format}"
        writer.writerow([sub1.content, sub2.content, f"[sound:{name}]"])
        os.system(f'ffmpeg -ss {str(start)} -to {str(end)} -i "{args.media}" -vn -acodec copy "{args.audio_dir}/{name}"')

def subtitles(args):
    time_delta=timedelta(milliseconds=args.delta_time)
    subs_src=list(parse_subs(args.source))
    subs_dst=list(parse_subs(args.target))
    for sub1 in subs_src:
        start_delta, j = min([(abs(sub2.start - sub1.start), i) for i, sub2 in enumerate(subs_dst)])
        end_delta, k = min([(abs(sub2.end - sub1.end), i) for i, sub2 in enumerate(subs_dst)])
        if start_delta <= time_delta and end_delta <= time_delta and k == j:
            yield (sub1, subs_dst[j])

def parse_subs(file):
    import srt
    content=file.read()
    if (name_ext := os.path.splitext(file.name)) and name_ext[1] == ".lrc":
        import pylrc
        return srt.parse(pylrc.parse(content).toSRT())
    else:
        return srt.parse(content)


if __name__ == "__main__":
    parser = ArgumentParser(description="a script to convert your media (movie/music) with two subtitles to csv data for anki, and audio files")
    parser.add_argument("--audio-dir", "-P", default=os.path.expanduser("~/.local/share/Anki2/User 1/collection.media/"))
    parser.add_argument("--target", "-t", type=FileType("r"), help="subtitle file for the target language (language to learn)")
    parser.add_argument("--source", "-s", type=FileType("r"), help="subtitle file for the source language (language that you already know)")
    parser.add_argument("--media", "-m", help="path to media file")
    parser.add_argument("--audio-format", "-f")
    parser.add_argument("--delta-time", type=int, default=600, help="delta to match subtitles with, in milliseconds. any two sub with difference larger than this delta would be ignored")
    parser.add_argument("output_csv", type=FileType("w"))
    main(parser.parse_args())
