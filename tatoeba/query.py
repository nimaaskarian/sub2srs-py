#!/usr/bin/env python3

import argparse
import csv
import os
import sqlite3

output_dir = 'output'
native_langs = []


def native_lang_columns():
        def native_lang_column(lang):
                return f"""
                "<ul class=""translations""><li>" ||
                (
                                SELECT group_concat(sentences.text, "</li><li>")
                                FROM links JOIN sentences
                                ON
                                                links.translation_id = sentences.sentence_id
                                WHERE
                                                links.sentence_id = target_sentences.sentence_id
                                                AND
                                                sentences.lang = '{lang}'
                                                )
                || "</li></ul>"
                """
        result = ""
        for lang in native_langs[:-1]:
                result += native_lang_column(lang) + ", "
        result += native_lang_column(native_langs[-1])
        return result


def main():
        parser = argparse.ArgumentParser(
                description="Make a CSV files of sentences from the Tatoeba Project that have audio, along with their translations into selected languages")
        parser.add_argument("-t", "--target", type=str,
                                                help="target language",
                                                required=True)
        parser.add_argument("-n", "--native", type=str,
                                                help="native languages (space-delimited, within quotes)",
                                                required=True)
        parser.add_argument("-d", "--database", type=str,
                                                help="database file",
                                                default = "tatoeba.sqlite3")
        args = parser.parse_args()
        global native_langs
        native_langs = args.native.split(" ")

        conn = sqlite3.connect(args.database)
        c = conn.cursor()

        query = f"""
        SELECT
                        target_sentences.sentence_id,
                        target_sentences.text,
                        "[sound:tatoeba_" || "{args.target}" || "_" || target_sentences.sentence_id || ".mp3]",
                        "<ul class=""tags""><li>" ||
                        (
                                SELECT group_concat(tag_name, "</li><li>")
                                FROM tags
                                WHERE tags.sentence_id = target_sentences.sentence_id
                        )
                        || "</li></ul>",
                        {native_lang_columns()}
        FROM
                        sentences AS target_sentences
        WHERE
                        target_sentences.lang = "{args.target}" AND
                        target_sentences.sentence_id IN (SELECT sentence_id FROM sentences_with_audio)
        ;
        """
        if not os.path.exists('output'):
                os.makedirs('output')
        with open(f'{os.path.join(output_dir, args.target)} → {args.native}.csv', 'w', newline='') as csvfile:
                out = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in c.execute(query):
                        out.writerow(row)

        conn.close()


if __name__ == '__main__':
        main()
