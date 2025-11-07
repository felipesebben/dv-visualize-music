from pathlib import Path
import music21 as m21

# --- 1. Define File Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

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


def main():
    """
    Main function to run the script.
    """

    file_path = find_musicxml_file(RAW_DATA_DIR)

    if file_path:
        print(f"\nFile finder is working. Path found: {file_path}.")
        # 'converter.parse' loads the file.
        # It can handle .mxl, .xml, and .mid files
        try:
            print("Loading and parsing the file with music21...")
            song = m21.converter.parse(file_path)
            
            print("\n--- SUCCESS! ---")
            print("File loaded and parsed successfully.")

            print("\n --- Reading Metadata ---")

            # The object has a '.metadata' attribute
            if song.metadata:
                print(f"    Song Title: {song.metadata.title}")
                print(f"    Composer: {song.metadata.composer}")
            else:
                print(" No metadata found in this file.")
        
            if song.parts:
                print(f"Found {len(song.parts)} parts (instruments in this file)")

                # Loop through each part and print their names.
                for part in song.parts:
                    print(f"    - Part Name: {part.partName}")
            
            else:
                print(" Could not find any parts in this file.")


        except Exception as e:
            print("\n--- ERROR ---")
            print(f"An error occurred while loading the file: {e}")
    
    else:
        print("\n--- TEST FAILED ---")
        print(f"File finder did not return a path")


if __name__ == "__main__":
    main()
