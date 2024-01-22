

import os
import argparse

def clean_folder(folder_path):
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
    except Exception as e:
        print(f"Error while cleaning folder: {e}")

def main():
    parser = argparse.ArgumentParser(description='Clean folder script')
    parser.add_argument('folder_path', help='Path to the folder to clean')
    args = parser.parse_args()
    
    clean_folder(args.folder_path)

if __name__ == "__main__":
    main()
