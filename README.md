# Anki-audiobook 🎧

Turn your [Anki](https://apps.ankiweb.net/) exports into an audiobook and make learning seamless during your workouts or sports routine. Whether you’re running, cycling, or lifting weights, this script keeps your mind sharp while staying active.

## Features
- Convert Anki exports into audio format using [Google Text-to-Speech](https://gtts.readthedocs.io/en/latest/).
- Learn effortlessly while on the go.
- Easy to use and lightweight script.

## Requirements
- Python 3.x
- An Anki export file as `.csv`

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/anki-audiobook.git
   cd anki-audiobook
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Example Usage
Run with:
   ```bash
   py main.py anki_vocabulary.csv
   ```

Or:
   ```bash
   py main.py -s -d r -m 5 anki_vocabulary.csv
   ```

## Help Output
Here is the output of the `--help` command for quick reference:

```
Usage: main.py [OPTIONS] FILENAME

  Creates an MP3 audiobook from an Anki vocabulary CSV file.

Options:
  -m, --max-per-track INTEGER   Maximum number of rows before the ouput file
                                will be splitted. 0 disables splitting.
                                [default: 0]
  -p, --pause-duration INTEGER  Duration of pause between sections in
                                milliseconds.  [default: 1000]
  -d, --direction [a|b|r]       Direction (a) left-to-right, (b) right-to-
                                left, (r) random   [default: a]
  -s, --shuffle                 Shuffle rows
  --help                        Show this message and exit.
```
