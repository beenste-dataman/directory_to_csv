import os
import pandas as pd
import argparse
import mimetypes
import pwd
import grp
import time

# Function to get file owner
def get_file_owner(file_path):
    try:
        stat_info = os.stat(file_path)
        uid = stat_info.st_uid
        gid = stat_info.st_gid
        user = pwd.getpwuid(uid).pw_name
        group = grp.getgrgid(gid).gr_name
        return f"{user} ({group})"
    except:
        return "Unknown"

# Function to recursively process the directory
def process_directory(directory, output_file):
    data = []

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_type = mimetypes.guess_type(file_path)[0] or "Unknown"
            parent_folder = os.path.basename(root)
            file_owner = get_file_owner(file_path)
            creation_time = time.ctime(os.path.getctime(file_path)) if hasattr(os.path, "getctime") else "N/A"
            last_modified_time = time.ctime(os.path.getmtime(file_path))

            data.append({
                "File Name": file,
                "File Type": file_type,
                "File Size": file_size,
                "Parent Folder": parent_folder,
                "Path to File": file_path,
                "Owner": file_owner,
                "Creation Date": creation_time,
                "Last Edited Date": last_modified_time,
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
