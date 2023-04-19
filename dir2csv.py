import os
import pandas as pd
from googletrans import Translator
import argparse
import mimetypes

# Function to recursively process the directory
def process_directory(directory, output_file):
    translator = Translator()
    data = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_type = mimetypes.guess_type(file_path)[0] or "Unknown"
            parent_folder = os.path.basename(root)
            translated_name = translator.translate(file, dest="en").text

            data.append({
                "File Name": file,
                "File Name Translated": translated_name,
                "File Type": file_type,
                "File Size": file_size,
                "Parent Folder": parent_folder,
                "Path to File": file_path,
            })

    # Create a DataFrame from the data and save it to a CSV file
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"CSV file has been saved to: {output_file}")

# Command line arguments for directory and output file
parser = argparse.ArgumentParser(description="Process a directory and save file info to a CSV file.")
parser.add_argument("directory", help="Directory path to process")
parser.add_argument("output_file", help="Output CSV file name")

args = parser.parse_args()

# Process the input directory and save the result to the output file
process_directory(args.directory, args.output_file)
