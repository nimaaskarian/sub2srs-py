#!/usr/bin/env python3
import os
from dataclasses import dataclass
from datetime import timedelta
from argparse import ArgumentParser, FileType

def main(args):
    import csv
    import subprocess
    if args.target_sid is not None:
        args.target = resolve_sid_to_tmp_file(args, args.target_sid)
    if args.source_sid is not None:
        args.source = resolve_sid_to_tmp_file(args, args.source_sid)

    writer = csv.writer(args.output_csv)
    for i, (sub1, sub2) in enumerate(subtitles(args)):
        start = min((sub1.start, sub2.start))
        end = max((sub1.end, sub2.end))
        print(str(start), str(end))
        base, _ = os.path.splitext(os.path.basename(args.input))
        name=f"sub2srs.py_{base}_{i+1}.{args.output_format}"
        writer.writerow([sub1.content, sub2.content, f"[sound:{name}]"])
        subprocess.run(['ffmpeg', '-ss', str(start), '-to', str(end), '-i', args.input]+args.ffmpeg_args+[f"{args.output_dir}/{name}"]).check_returncode()

def subtitles(args):
    time_delta=timedelta(milliseconds=args.delta_time)
    subs_src=list(parse_subs(args.source))
    subs_dst=list(parse_subs(args.target))
    for sub1 in subs_src:
        start_delta, j = min([(abs(sub2.start - sub1.start), i) for i, sub2 in enumerate(subs_dst)])
        end_delta, k = min([(abs(sub2.end - sub1.end), i) for i, sub2 in enumerate(subs_dst)])
        if start_delta <= time_delta and end_delta <= time_delta and k == j:
            yield (sub1, subs_dst[j])

def resolve_sid_to_tmp_file(args,sid):
    import tempfile
    import subprocess
    path = tempfile.mktemp(suffix=".srt")
    subprocess.run(["ffmpeg", "-i", args.input, "-map" f"0:s:{sid}", path]).check_returncode()
    return open(path, "r")

def parse_subs(file):
    import srt
    content=file.read()
    if (name_ext := os.path.splitext(file.name)) and name_ext[1] == ".lrc":
        return parse_lrc(content)
    else:
        return srt.parse(content)

def parse_lrc(content: str):
    from datetime import datetime, time
    lines = content.splitlines()
    output_lines = []
    for i, line in enumerate(lines):
        timestr, content = line.split("]", maxsplit=1)
        parsed_time = None
        for format in ("[%H:%M:%S.%f", "[%M:%S.%f"):
            try:
                t = datetime.strptime(timestr,format)
                parsed_time = t - datetime.combine(t.date(), time.min)
            except ValueError:
                pass
        if parsed_time is None:
            raise ValueError("invalid timestamp")

        if content.strip() == "":
            output_lines.append(None)
        else:
            output_lines.append(LrcLine(parsed_time, None, content))

        if i > 0 and output_lines[i-1] is not None:
            output_lines[i-1].end = parsed_time
    output_lines = [line for line in output_lines if line is not None]
    if output_lines[-1].end is None:
        output_lines[-1].end = output_lines[-1].start + timedelta(seconds=5)

    return output_lines

@dataclass
class LrcLine:
    start: timedelta
    end: timedelta | None
    content: str



if __name__ == "__main__":
    parser = ArgumentParser(description="a script to convert your media (movie/music) with two subtitles to csv data for anki, and audio files")
    parser.add_argument("--output-dir", "-P", default=os.path.expanduser("~/.local/share/Anki2/User 1/collection.media/"))
    targets = parser.add_mutually_exclusive_group()
    sources = parser.add_mutually_exclusive_group()
    targets.add_argument("--target", "-t", type=FileType("r"), help="subtitle file for the target language (language to learn)")
    targets.add_argument("--target-sid", "-T", default=None, type=int, help="target language subtitle id (first subtitle's sid is 0)")
    sources.add_argument("--source", "-s", type=FileType("r"), help="subtitle file for the source language (language that you already know)")
    sources.add_argument("--source-sid", "-S", default=None, type=int, help="source language subtitle id (first subtitle's sid is 0)")
    parser.add_argument("--ffmpeg-args", "-F", nargs="+", action="append", default=None, help="additional arguments to pass to ffmpeg. defaults to `-vn -acodec`. prefer to specify at the end of the command")
    parser.add_argument("--input", "-i", help="path to input media file")
    parser.add_argument("--append", "-a", action="store_true", help="append to the output_csv instead of overwriting it")
    parser.add_argument("--output-format", "-f")
    parser.add_argument("--delta-time", type=int, default=600, help="delta to match subtitles with, in milliseconds. any two sub with difference larger than this delta would be ignored. the lower this value, the more accurate the outpu. the lower this value, the more accurate the output")
    parser.add_argument("output_csv")
    args = parser.parse_args()

    args.output_csv = open(args.output_csv, "a" if args.append else "w")
    if args.ffmpeg_args is None:
        args.ffmpeg_args = ['-vn', '-acodec', 'copy']


    main(args)
