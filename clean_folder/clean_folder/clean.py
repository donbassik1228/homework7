from pathlib import Path
import shutil
import re
import sys

IMAGES = list()  
DOCS = list()  
VIDEO = list()  
MUSIC = list()  
ARCHIVES = list()
OTHER = list()
Folders = list()
Unknown = set()
Extensions = set()

registered_extensions = {'JPEG' : IMAGES, 'PNG' : IMAGES, 'JPG' : IMAGES, 'SVG' : IMAGES,
                         'AVI' : VIDEO, 'MP4' : VIDEO, 'MOV' : VIDEO, 'MKV' : VIDEO,
                         'TXT' : DOCS, 'DOCX' : DOCS, 'DOC' : DOCS, 'PDF' : DOCS, 'XLSX': DOCS, 'PPTX': DOCS,
                         'MP3' : MUSIC, 'OGG' : MUSIC, 'WAV' : MUSIC, 'AMR' : MUSIC, 
                         'ZIP' : ARCHIVES, 'GZ' : ARCHIVES, 'TAR' : ARCHIVES      
                        }

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()

def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"




def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('JPEG', 'PNG', 'JPG', 'SVG', 'AVI', 'MP4', 'MOV', 'MKV', 'TXT', 'DOCX',\
                                 'DOC', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV', 'AMR', 'ARCHIVE', 'OTHER'):
                Folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder/item.name
        if not extension:
            OTHER.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                Extensions.add(extension)
                container.append(new_name)
            except KeyError:
                Unknown.add(extension)
                OTHER.append(new_name)


    print(f"Images: {IMAGES}")
    print(f"Vide: {VIDEO}")
    print(f"Docs: {DOCS}")
    print(f"Music: {MUSIC}")
    print(f"Archive: {ARCHIVES}")
    print(f"Other: {OTHER}")
    print(f"All extensions: {Extensions}")
    print(f"Unknown extensions: {Unknown}")
    print(f"Folder: {Folders}")


    
def handle_file(path, root_folder, dist):
    target_folder = root_folder/dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize(path.name.replace(".zip", ''))

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), str(archive_folder.resolve()))
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def main():
    if len(sys.argv) != 2:
        print("Usage: python clean.py <folder_path>")
        sys.exit(1)

    folder_path = Path(sys.argv[1])
    print(folder_path)
    scan(folder_path)

    for file in IMAGES:
        handle_file(file, folder_path, "Images")

    for file in VIDEO:
        handle_file(file, folder_path, "Video")

    for file in DOCS:
        handle_file(file, folder_path, "Docs")

    for file in MUSIC:
        handle_file(file, folder_path, "Music")

    for file in OTHER:
        handle_file(file, folder_path, "Other")

    for file in ARCHIVES:
        handle_archive(file, folder_path, "Archive")

    remove_empty_folders(folder_path)

if __name__ == '__main__':
    main()