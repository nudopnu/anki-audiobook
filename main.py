import csv
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

def create_audiobook(csv_file, output_file, pause_duration=1000):
    """
    Creates an audiobook from an Anki vocabulary CSV file.

    Parameters:
        csv_file (str): Path to the CSV file with vocabulary.
        output_file (str): Path to save the audiobook.
        pause_duration (int): Pause duration between items in milliseconds.
    """
    # Load vocabulary from CSV
    vocabulary = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            if len(row) >= 2:  # Ensure each row has at least two columns
                vocabulary.append((row[0].strip(), row[1].strip()))

    # Initialize the audiobook
    audiobook = AudioSegment.silent(duration=0)

    for term, definition in vocabulary:
        # Generate audio for term
        term_audio = gTTS(text=term, lang='en')
        term_audio_file = "term.mp3"
        term_audio.save(term_audio_file)
        term_segment = AudioSegment.from_file(term_audio_file)

        # Generate audio for definition
        definition_audio = gTTS(text=definition, lang='en')
        definition_audio_file = "definition.mp3"
        definition_audio.save(definition_audio_file)
        definition_segment = AudioSegment.from_file(definition_audio_file)

        # Add term, pause, and definition to the audiobook
        audiobook += term_segment
        audiobook += AudioSegment.silent(duration=pause_duration)
        audiobook += definition_segment
        audiobook += AudioSegment.silent(duration=pause_duration * 2)  # Longer pause between items

        # Clean up temporary files
        os.remove(term_audio_file)
        os.remove(definition_audio_file)

    # Export the final audiobook
    audiobook.export(output_file, format="mp3")
    print(f"Audiobook saved to {output_file}")

# Example usage
# Provide the path to your Anki CSV file and the desired output file path.
create_audiobook("anki_vocabulary.csv", "anki_audiobook.mp3")
