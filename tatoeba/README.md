anki autism setup

```bash
# these need to be run only one time for all the languages.
# the data base is shared across all languages
./download-tatoeba-csv.sh 
sqlite3 -init make-db.sql

# deu is the target language in this example
./download-audio.sh deu tatoeba.sqlite3 &
# -n's optarg is space seperated list of all the output languages
./query.py -t deu -n eng
```
