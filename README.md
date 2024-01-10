# JMG Laion Utilies
A bunch of scripts that can be used when working with the Laion data set. Assumes Laion has been downloaded using [img2dataset](https://github.com/rom1504/img2dataset) as this tends to output the data set in the following format:

- shard_id
    - 0000.jpg
    - 0000.txt
    - 0000.json


## List of available utils
### Simple data set csv creation
- Given a directory with a similar layout to the above, this script will create a CSV file containing *N* random entries from the data set and save it. The CSV file will contain the following:
    1. The id of data set entry.
    2. The caption of the entry.
    3. The path to the image assoicated with the entry

#### Program Arugments
The ``--laion_dir``, ``--n_entries`` and ``--out_file`` arguments are required, the ``--seed`` argument is optional (default=42).

``python img_text_csv_creation.py  --laion_dir PATH/TO/DATA --n_entries N --out_file PATH/TO/OUT.csv --seed SOME_SEED``
