import csv
from gtts import gTTS
from pydub import AudioSegment
import os
import click
import random

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('-m', '--max-per-track', default=0, type=int, show_default=True, help='Maximum number of rows before the ouput file will be splitted. 0 disables splitting.')
@click.option('-p', '--pause-duration', default=1000, type=int, show_default=True, help='Duration of pause between sections in milliseconds.')
@click.option('-d', '--direction', default='a', type=click.Choice(['a', 'b', 'r'], case_sensitive=False), show_default=True, help='Direction (a) left-to-right, (b) right-to-left, (r) random ')
@click.option('-s', '--shuffle', default=False, type=bool, is_flag=True, show_default=True, help='Shuffle rows')
def main(filename: str, max_per_track: int, pause_duration: int, direction: str, shuffle: bool):
    """
    Creates an MP3 audiobook from an Anki vocabulary CSV file.
    """
    # Load vocabulary from CSV
    vocabulary = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if len(row) >= 2:  # Ensure each row has at least two columns
                vocabulary.append((row[0].strip(), row[1].strip()))
    
    # Optionally shuffle the vocabulary
    if shuffle:
        random.shuffle(vocabulary)

    # Get base name for output file(s)
    basename, _ = os.path.splitext(filename)
    output_file = f"{basename}.mp3"

    # Initialize the audiobook
    audiobook = AudioSegment.silent(duration=0)
    part = 1

    for idx, (term, definition) in enumerate(vocabulary):
        # Generate audio for term in English
        term_audio = gTTS(text=term, lang='en')
        term_audio_file = "term.mp3"
        term_audio.save(term_audio_file)
        term_segment = AudioSegment.from_file(term_audio_file)

        # Generate audio for definition in German
        definition_audio = gTTS(text=definition, lang='de')
        definition_audio_file = "definition.mp3"
        definition_audio.save(definition_audio_file)
        definition_segment = AudioSegment.from_file(definition_audio_file)

        # Optionally switch term and definition
        if direction == 'b' or direction == 'r' and random.random() > 0.5:
            term_segment, definition_segment = definition_segment, term_segment

        # Add term, pause, and definition to the audiobook
        audiobook += term_segment
        audiobook += AudioSegment.silent(duration=pause_duration)
        audiobook += definition_segment
        audiobook += AudioSegment.silent(duration=pause_duration)

        # Clean up temporary files
        os.remove(term_audio_file)
        os.remove(definition_audio_file)

        # Split file if necessary
        if max_per_track == 0 or idx == 0 or idx % max_per_track != 0:
            continue
        output_file = f"{basename}_{part:03d}.mp3"
        part += 1
        audiobook.export(output_file, format="mp3")
        audiobook = AudioSegment.silent(duration=0)
        output_file = f"{basename}_{part:03d}.mp3"

    # Export the final audiobook
    audiobook.export(output_file, format="mp3")
    print(f"Audiobook saved to {output_file}")

if __name__ == "__main__":
    main()