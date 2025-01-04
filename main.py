import csv
from gtts import gTTS
from pydub import AudioSegment
import os
import click

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--max-per-track', default=0, type=int, help='Maximum number of tracks before the ouput file will be splitted.')
@click.option('--pause-duration', default=1000, type=int, help='Duration of pause between sections in milliseconds.')
def main(filename, output_file, max_per_track, pause_duration):
    """
    Creates an audiobook from an Anki vocabulary CSV file.
    """
    # Load vocabulary from CSV
    vocabulary = []
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if len(row) >= 2:  # Ensure each row has at least two columns
                vocabulary.append((row[0].strip(), row[1].strip()))

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
        output_file = f"out_{part:03d}.mp3"
        part += 1
        audiobook.export(output_file, format="mp3")
        audiobook = AudioSegment.silent(duration=0)
        output_file = f"out_{part:03d}.mp3"

    # Export the final audiobook
    audiobook.export(output_file, format="mp3")
    print(f"Audiobook saved to {output_file}")

if __name__ == "__main__":
    main()