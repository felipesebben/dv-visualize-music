import pretty_midi
import pandas as pd
from pathlib import Path

# --- 1. Define file paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

def find_midi_file(search_dir):
    """
    Searches a directory for exactly one MIDI file.
    """
    print(f"Searching for MIDI files in: {search_dir}")

    midi_files = list(search_dir.glob("*.mid*"))

    # --- 3. Check identified files ---
    if len(midi_files) == 0:
        print("\n--- ERROR ---")
        print(f"No MIDI files (.mid or .midi) found in {search_dir}.")
        return None # Return nothing if no file

    elif len(midi_files) > 1:
        print("\n--- ERROR ---")
        print(f"Found {len(midi_files)}. Please put only *one* file in {search_dir}.")
        return None # Return nothing if too many files

    else:
        file_to_load = midi_files[0] # Get the one file from the list
        print(f"Found one file: {file_to_load.name}")
        return file_to_load
    
def extract_note_data(midi_data):
    """
    Loops through all instruments and notes, returning a list of dictionaries.
    """
    all_notes = []

    print(f"Processing {len(midi_data.instruments)} instrument tracks...")

    for i, instrument in enumerate(midi_data.instruments):

        # Get the instrument name
        instrument_name = pretty_midi.program_to_instrument_name(instrument.program)

        # Loop over all notes for this instrument
        for note in instrument.notes:
            
            # Get all the data for this single note
            note_data = {
                "track_index": i,
                "track_name": instrument.name,
                "instrument": instrument_name,
                "is_drum": instrument.is_drum,
                "pitch_num": note.pitch,
                "start_time_sec": note.start,
                "end_time_sec": note.end,
                "duration_sec": note.duration,
                "velocity": note.velocity
            }

            # Add this note's data to our list
            all_notes.append(note_data)
    print(f"Successfully extracted {len(all_notes)} total notes")
    return all_notes

def main():
    """
    Main function to run the script.
    """
    file_path = find_midi_file(RAW_DATA_DIR)

    if file_path: # Only proceed if we found a file
        try:
            midi_data = pretty_midi.PrettyMIDI(str(file_path))
            print("File loaded successfully.")

            all_note_data = extract_note_data(midi_data)

            if all_note_data:
                print("\n--- SUCCESS! ----")
                print(f"First 5 notes extracted:")
                for note in all_note_data[0:5]:
                    print(note)

        except Exception as e:
            print(f"\nAn error occurred while loading the file: {e}")

if __name__ == "__main__":
    main()