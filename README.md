# DuplicateDetector
DuplicateDetector is a Python-based command-line interface tool that helps you detect duplicate files on your system. It works on all major operating systems, including Windows, Linux, and MacOS.

## Installation
Clone this repository and run the `duplicatedetector.py` file in a Python environment.

## Usage
```shell
python DuplicateDetector.py [directory]
```

### Arguments
    `directory`: The directory to scan for duplicate files.

If no directory is specified, DuplicateDetector will scan the current directory.

## How it works
DuplicateDetector uses the `os`, `hashlib`, and `datetime` Python modules to find duplicate files on your system.

First, it walks through the specified directory and its subdirectories to hash each file's content using the `hash_file()` function. It then stores the file path in two dictionaries, `files_hash` and `filenames`, based on its hash and filename, respectively.

It then finds files with duplicate content and filenames but unique content, and sorts them by their creation and modification timestamps. Finally, it prints the duplicates in a user-friendly way.

## Example
```shell
python duplicatedetector.py ~/Documents
```

This will scan the Documents directory for duplicate files and print the duplicates.
