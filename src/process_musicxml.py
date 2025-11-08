from pathlib import Path
import music21 as m21
import pandas as pd

# --- 1. Define File Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

def  find_musicxml_file(search_dir):
    """
    Searches a directory for exactly one MusicXML file.
    """
    print(f"Searching for MusicXML files in: {search_dir}")

    # Search for .musicxml Or .xml
    xml_files = list(search_dir.glob("*.musicxml"))
    xml_files.extend(list(search_dir.glob("*.mxl"))) # Append .mxl to list
    xml_files.extend(list(search_dir.glob("*.xml"))) # Append .xml to list

    if len(xml_files) == 0:
        print("\n--- ERROR ---")
        print(f"No MusicXML files (.musicxml, .xml, or .mxl) found in '{search_dir}'.")
        return None

    elif len(xml_files) > 1:
        print(f"\n--- ERROR ---")
        print(f"Found {len(xml_files)} MusicXML files. please put only *one* file in {search_dir}.")
        return None
    
    else:
        file_to_load = xml_files[0]
        print(f"Found one file: {file_to_load.name}")
        return file_to_load

def extract_musicxml_data(score):
    """
    Loops through all parts in the score and extracts data.
    """
    print("\n--- Extracting Data from All Parts ---")

    # Empty list to hold the list of dictionaries
    all_data = []

    # Outer loop - iterate over each instrument part
    for i, part in enumerate(score.parts):
        print(f"    - Processing Part {i +1}/{len(score.parts)}: {part.partName}")

        # Get all notes, chords, and rests from the iterated part
        all_items = part.flatten().notesAndRests

        # Iterate over each item (note/chord/rest)
        for item in all_items:

            # Case 1: the item is a single note
            if isinstance(item, m21.note.Note):
                note_data = {
                    "part_index": i,
                    "part_name": part.partName,
                    "type": "Note",
                    "pitch_name": item.nameWithOctave,
                    "pitch_simple": item.pitch.name,
                    "octave": item.pitch.octave,
                    "beat": item.beat,
                    "duration_beats": item.duration.quarterLength,
                    "offset_beats": item.offset,
                }
                all_data.append(note_data)
            
            # Case 2: the item is a chord
            if isinstance(item, m21.chord.Chord):
                # Loop through each note and add a separate row for each note in the chord.
                for pitch in item.pitches:
                    note_data = {
                        "part_index": i,
                        "part_name": part.partName,
                        "type": "Chord Note",
                        "pitch_name": pitch.nameWithOctave,
                        "pitch_simple": pitch.name,
                        "octave": pitch.octave,
                        "beat": item.beat,
                        "duration_beats": item.duration.quarterLength,
                        "offset_beats": item.offset,
                    }
                    all_data.append(note_data)

    print(f"--- Finished processing. Found {len(all_data)} total notes. ---")
    return all_data

def clean_dataframe(df):
    """
    Cleans the DataFrame, converting data types.
    """
    print(f"\n--- Cleaning DataFrame ---")

    # Define columns that should be numbers
    numeric_cols = ["beat", "duration_beats", "offset_beats"]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    
    print(f"DataFrame successfully cleaned.")
    return df

def save_data_to_csv(df, output_dir, file_name):
    """
    Saves a DataFrame to a CSV file in a specified directory.
    """
    print("\n--- Saving Cleaned DataFrame to CSV ---")

    # Ensure the directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Define the full path for the file
    output_path = output_dir / file_name

    # Save the df to CSV
    df.to_csv(output_path, index=False)

    print("--- Success! ---")
    print(f"Clean data saved to: {output_path}")

def main():
    """
    Main function to run the script.
    """

    file_path = find_musicxml_file(RAW_DATA_DIR)

    if file_path:
        print(f"\nFile finder is working. Path found: {file_path}.")

        try:
            print("Loading and parsing the file with music21...")
            score = m21.converter.parse(file_path)
            
            print("\n--- SUCCESS! ---")
            print("File loaded and parsed successfully.")

            all_note_data = extract_musicxml_data(score)

            if all_note_data:
                print("\n--- Converting to DataFrame ---")

                df_raw = pd.DataFrame(all_note_data)

                # Pass the raw df to the cleaning function
                df_clean = clean_dataframe(df_raw)
 
                # Save the clean DataFrame
                save_data_to_csv(df_clean, PROCESSED_DATA_DIR, "rhcp-dosed_musicmxl_notes.csv")

                print("\n--- Pipeline Complete ---")
                print("Final DataFrame .head() preview:")
                print(df_clean.head())
                
        except Exception as e:
            print("\n--- ERROR ---")
            print(f"An error occurred while loading the file: {e}")
    
    else:
        print("\n--- TEST FAILED ---")
        print(f"File finder did not return a path")


if __name__ == "__main__":
    main()
