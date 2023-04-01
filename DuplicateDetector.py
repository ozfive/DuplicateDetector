import os
import hashlib
from datetime import datetime
import argparse
from collections import defaultdict
import time

def get_file_timestamps(file_path):
    create_time = os.path.getctime(file_path)
    modified_time = os.path.getmtime(file_path)
    return create_time, modified_time

def hash_file(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        buf = file.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file.read(65536)
    return hasher.hexdigest()

def find_duplicate_files(directory):
    # Create defaultdicts to store file hashes and filenames
    files_hash = defaultdict(list)
    filenames = defaultdict(list)

    # Walk through the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = hash_file(file_path)

            # Store the file path in the files_hash dictionary based on its hash
            files_hash[file_hash].append(file_path)

            # Store the file path in the filenames dictionary based on its filename
            filenames[file].append(file_path)

    # Initialize dictionaries to store duplicate files and filenames
    duplicate_files = {}
    duplicate_filenames = {}

    # Find files with duplicate content
    for file_hash, files in files_hash.items():
        if len(files) > 1:
            # Sort the files by creation and modification timestamps
            sorted_files = sorted(files, key=lambda f: get_file_timestamps(f)[0] or get_file_timestamps(f)[1])
            duplicate_files[file_hash] = sorted_files

    # Find files with duplicate filenames but unique content
    for filename, filepaths in filenames.items():
        if len(filepaths) > 1:
            file_hashes = [hash_file(filepath) for filepath in filepaths]

            # Check if all file hashes are unique, indicating unique content
            if len(set(file_hashes)) == len(filepaths):
                # Sort the files by creation and modification timestamps
                sorted_files = sorted(filepaths, key=lambda f: get_file_timestamps(f)[0] or get_file_timestamps(f)[1])
                duplicate_filenames[filename] = sorted_files

    return duplicate_files, duplicate_filenames

def print_duplicates(files, category):
    sorted_files = sorted(files, key=lambda f: get_file_timestamps(f)[0] or get_file_timestamps(f)[1])
    print(f'Original:   {sorted_files[0]} (Created: {datetime.fromtimestamp(os.path.getctime(sorted_files[0])).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(sorted_files[0])).strftime("%Y-%m-%d %H:%M:%S")}) [{category}]')
    for file in sorted_files[1:]:
        print(f'Duplicate:  {file} (Created: {datetime.fromtimestamp(os.path.getctime(file)).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(file)).strftime("%Y-%m-%d %H:%M:%S")}) [{category}]')
    print()

def main():
    parser = argparse.ArgumentParser(description='Find duplicate files in a directory.')
    parser.add_argument('directory', help='Directory to scan for duplicate files')

    args = parser.parse_args()

    duplicate_files, duplicate_filenames = find_duplicate_files(args.directory)

    filename_and_content_sets = set()
    print('Duplicate files (filename and content):')
    for file_hash, files in duplicate_files.items():
        if len(files) > 1:
            for i, file1 in enumerate(files):
                for file2 in files[i + 1:]:
                    if os.path.basename(file1) == os.path.basename(file2):
                        print(f'Original:   {file1} (Created: {datetime.fromtimestamp(os.path.getctime(file1)).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(file1)).strftime("%Y-%m-%d %H:%M:%S")}) [Filename and Content]')
                        print(f'Duplicate:  {file2} (Created: {datetime.fromtimestamp(os.path.getctime(file2)).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(file2)).strftime("%Y-%m-%d %H:%M:%S")}) [Filename and Content]')
                        print()


    print('\nDuplicate filenames:')
    for filename, filepaths in duplicate_filenames.items():
        if len(filepaths) > 1:
            file_hashes = [hash_file(filepath) for filepath in filepaths]
            if len(set(file_hashes)) == len(filepaths):
                print(f'Filename: {filename}')
                sorted_files = sorted(filepaths, key=lambda f: get_file_timestamps(f)[0] or get_file_timestamps(f)[1])
                print(f'Original:   {sorted_files[0]} (Created: {datetime.fromtimestamp(os.path.getctime(sorted_files[0])).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(sorted_files[0])).strftime("%Y-%m-%d %H:%M:%S")})')
                for filepath in sorted_files[1:]:
                    print(f'Duplicate:  {filepath} (Created: {datetime.fromtimestamp(os.path.getctime(filepath)).strftime("%Y-%m-%d %H:%M:%S")} | Modified: {datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")}) [Filenames Only]')

    print('\nDuplicate content:')
    printed_content_duplicates = set()
    for file_hash, files in duplicate_files.items():
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                if os.path.basename(file1) != os.path.basename(file2) and file1 not in printed_content_duplicates and file2 not in printed_content_duplicates:
                    printed_content_duplicates.add(file1)
                    printed_content_duplicates.add(file2)
                    print_duplicates([file1, file2], "Content Only")

if __name__ == '__main__':
    main()
