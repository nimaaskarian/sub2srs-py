.open tatoeba.sqlite3

-- Tatoeba’s database has many deleted entries in `sentences` which are referenced from `sentences_with_audio` and `links`; expect tons of warning messages
PRAGMA foreign_keys = ON;

CREATE TABLE sentences (
        sentence_id INTEGER PRIMARY KEY,
        lang TEXT,
        text TEXT
);
CREATE TABLE sentences_with_audio (
        sentence_id INTEGER PRIMARY KEY,
        username TEXT,
        license TEXT,
        attribution_url TEXT,
        FOREIGN KEY (sentence_id) REFERENCES sentences(sentence_id)
);
CREATE TABLE links (
        sentence_id INTEGER,
        translation_id INTEGER,
        FOREIGN KEY (sentence_id) REFERENCES sentences(sentence_id),
        FOREIGN KEY (translation_id) REFERENCES sentences(sentence_id)
);
CREATE TABLE tags (
        sentence_id INTEGER,
        tag_name TEXT,
        FOREIGN KEY (sentence_id) REFERENCES sentences(sentence_id)
);

CREATE INDEX links_index ON links(sentence_id, translation_id);
CREATE INDEX tags_index ON tags(sentence_id, tag_name);

.separator "\t"
.import csv/sentences.escaped_quotes.csv sentences
.import csv/sentences_with_audio.uniq.csv sentences_with_audio
.import csv/links.csv links
.import csv/tags.escaped_quotes.csv tags
