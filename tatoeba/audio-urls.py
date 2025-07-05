#!/usr/bin/env python3

import argparse
import csv
import sqlite3


def main():
        parser = argparse.ArgumentParser(
                description="Make a list of URLs of audio files for a specific language from the Tatoeba Project")
        parser.add_argument("-t", "--target", type=str,
                                                help="target language",
                                                required=True)
        parser.add_argument("-d", "--database", type=str,
                                                help="database file",
                                                default = "tatoeba.sqlite3")
        args = parser.parse_args()

        conn = sqlite3.connect(args.database)
        c = conn.cursor()

        query = f"""
SELECT
        sentence_id
FROM
        sentences
WHERE
        lang = '{args.target}' AND
        sentence_id IN (SELECT sentence_id FROM sentences_with_audio)
        """

        for row in c.execute(query):
                print("https://audio.tatoeba.org/sentences/" + args.target + "/" + str(row[0]) + ".mp3")


if __name__ == '__main__':
        main()
