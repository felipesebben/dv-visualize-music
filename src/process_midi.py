import pretty_midi
from pathlib import Path

# --- 1. Define file paths ---
# Create a Path object for the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

print(BASE_DIR)

# Define the directory path
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

print(f"Project base directory: {BASE_DIR}")
print(f"Searching for MIDI files in: {RAW_DATA_DIR}")

# --- 2. Find the File ---
# Use glob() to find any file ending in .mid or .midi
midi_files = list(RAW_DATA_DIR.glob("*.mid*"))

# --- 3. Check identified files ---
if len(midi_files) == 0:
    print("\n--- ERROR ---")
    print(f"No MIDI files (.mid or .midi) found in {RAW_DATA_DIR}.")
    print(f"Please add your MIDI file to that folder.")

elif len(midi_files) > 1:
    print("\n--- ERROR ---")
    print(f"Found {len(midi_files)}. Please put only *one* file in {RAW_DATA_DIR}.")
    for f in midi_files:
        print(f"    - {f.name}")

else:
    file_to_load = midi_files[0] # Get the one file from the list
    print(f"Found one file: {file_to_load.name}")

    # --- 4. Load the file ---
    try:
        midi_data = pretty_midi.PrettyMIDI(str(file_to_load))

        print(f"\n--- Sucess! ---")
        print(f"File loaded successfully.")
        print(f"Found {len(midi_data.instruments)} instrument tracks.")
    
    except Exception as e:
        print(f"\nAn error occurred while loading the file: {e}")